from __future__ import annotations

import json
from functools import partial
from typing import TYPE_CHECKING, Protocol

from pyodide.http import pyfetch

from .drag_drop_grid_controller import DragDropGridController
from .image_grid_controller import ImageGridController
from .rotating_images_controller import RotatingImagesController

if TYPE_CHECKING:
    from collections.abc import Callable

    from js import JsDomElement, JsInputElement

    from protocol import Solution, SolutionRequest, SolutionResponse, TilesResponse


class Controller(Protocol):
    """A generic controller that manages a set of images inside a captcha."""

    @property
    def solution(self) -> Solution:
        """The current solution in a suitable format.

        Returns
        -------
        list[tuple[int, float]] | list[int] | list[float]
            Any one of:
              - List of tuples where each tuple contains the position and rotation of each image.
                Each tuple is in the format (position, rotation).
              - List of indices representing the current order of images in the grid.
              - List of rotation values in degrees.
        """
        ...

    def render(self, images: list[str], /) -> None:
        """Render the images in the captcha.

        Parameters
        ----------
        images:
            List of base64 encoded strings to be displayed in the grid.
        """
        ...

    def reset(self) -> None:
        """Reset the captcha to its initial state."""
        ...

    def destroy(self) -> None:
        """Remove the captcha and all child elements from the root, resetting its styles."""
        ...


CONTROLLER_FACTORIES: dict[str, Callable[[JsDomElement], Controller]] = {
    "grid": ImageGridController,
    "rows": DragDropGridController,
    "circle": partial(RotatingImagesController, rotation_steps=6),
}


async def fetch_tiles() -> TilesResponse:
    """Fetch tile images and their associated type for CAPTCHA challenges.

    This function makes an asynchronous request to the `/api/tiles` endpoint
    and retrieves a collection of tile images and their associated type. The response
    is structured to contain the tile type (e.g., 'grid', 'rows', 'circles') and the
    corresponding tile image URIs.

    Returns
    -------
    TilesResponse
        A dictionary containing the type of CAPTCHA and a list of image URIs.

    Raises
    ------
    RuntimeError
        If the request to the `/api/tiles` endpoint fails.
    """
    response = await pyfetch("/api/tiles")
    if not response.ok:
        # Need to properly handle errors
        msg = f"Failed to fetch images: {response.status} {await response.string()}"
        raise RuntimeError(msg)

    return await response.json()


async def post_solution(solution: Solution, code: str) -> bool:
    """Post a proposed CAPTCHA solution to the server and retrieve the verification result.

    This function sends an asynchronous request to the `/api/solution` endpoint, passing
    the given solution for verification. The server responds with a boolean indicating
    whether the proposed solution is correct or not.

    Parameters
    ----------
    solution:
        The proposed CAPTCHA solution generated by the user's interactions.

    Returns
    -------
    bool
        `True` if the solution is correct, `False` otherwise.

    Raises
    ------
    RuntimeError
        If the request to the `/api/solution` endpoint fails.
    """
    body: SolutionRequest = {
        "code": code,
        "solution": solution,
    }

    response = await pyfetch(
        "api/solution",
        method="POST",
        headers={"Content-Type": "application/json"},
        body=json.dumps(body),
    )

    if not response.ok:
        # Need to properly handle errors
        msg = f"Failed to post solution: {response.status} {await response.string()}"
        raise RuntimeError(msg)

    response_body: SolutionResponse = await response.json()

    return response_body["solved"]


class App:
    """The primary application controller managing the UI.

    Attributes
    ----------
    active_controller : Controller | None
        The currently active controller handling UI interactions.
        Can be None if no controller is set.
    code_input : JsInputElement
        The text input element where the user types the code from the image.
    root : JsDomElement
        The main DOM element that the app and its controllers interact with.
    """

    def __init__(self, root: JsDomElement, code_input: JsInputElement) -> None:
        self.active_controller: Controller | None = None
        self.code_input: JsInputElement = code_input
        self.root: JsDomElement = root

    async def load_captcha(self) -> None:
        """Load and display a CAPTCHA challenge using the appropriate controller.

        This method fetches a new CAPTCHA challenge from the server, which comprises a type
        (e.g., 'grid', 'rows', 'circles') and a set of associated tile images. Depending on
        the CAPTCHA type, it transitions to the corresponding controller and instructs it
        to render the fetched tiles.
        """
        captcha = await fetch_tiles()

        controller_name = captcha["type"]
        tiles = captcha["tiles"]

        self.code_input.value = ""
        self.set_controller(controller_name)

        if self.active_controller is not None:
            self.active_controller.render(tiles)

    async def post_solution(self) -> bool:
        """Post the current solution and return whether or not it's correct.

        Returns
        -------
        bool
            `True` if the current solution is correct, `False` if otherwise.
        """
        result = False

        if self.active_controller is not None:
            result = await post_solution(self.active_controller.solution, self.code_input.value)

        return result

    def reset(self) -> None:
        """Restore the active controller to its original state and clear the input field."""
        self.code_input.value = ""
        if self.active_controller is not None:
            self.active_controller.reset()

    def set_controller(self, controller_name: str) -> None:
        """Transition to the active controller identified by the provided name.

        This method will destroy the previously active controller (if any), fetch the required
        images, and then render the new controller using those images.

        Parameters
        ----------
        controller_name:
            The identifier for the desired controller.
            Must match a key in the `controller_factories` dictionary.
        """
        if self.active_controller is not None:
            self.active_controller.destroy()

        if controller_name not in CONTROLLER_FACTORIES:
            return

        controller_factory = CONTROLLER_FACTORIES[controller_name]
        self.active_controller = controller_factory(self.root)
