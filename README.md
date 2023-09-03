# Digital Shadows

**Digital Shadows** transports players into the enthralling depths of the digital realm, bridging the gap
between the online world and palpable real-world locations, ranging from underground hacker dens and
abandoned warehouses to fortified safehouses.

In the game's opening cinematic, the narrative unfolds on a screen shrouded in darkness, gradually
illuminated by cascading lines of mysterious code. As the climax of this digital downpour is reached,
players are introduced to the central character: Eclipse is a master hacker known only by this codename.
An encrypted message demands Eclipse's attention within a dimly lit enclave, awash with the glow of myriad screens:
"They're making a move. The web is tightening. Need your skills."

Eclipse's enigmatic past reveals a hacker who once operated on the digital periphery. Their trajectory
dramatically shifts upon being recruited by an elite international cybersecurity group. But lurking in
the backdrop is the game's menacing antagonist: "The Silent Hand," a sinister terrorist collective skilled
in wielding advanced digital tools to sow real-world chaos.

Embarking on the Digital Shadows journey, players are tasked with deciphering a complex array of digital
puzzles. Every riddle unraveled delves deeper into the dark web, uncloaking encrypted data and unwinding
layers of secretive communication. Successive solutions unravel the plots and expose the identities of
the shadowy faction, drawing Eclipse ever closer to thwarting "The Silent Hand."

Dive deep into this entwining of shadows, where the boundaries between the digital and tangible blur, and
every decision could reveal a hidden secret or set off an unseen trap. Brace yourself, for in this world,
shadows are always vigilant.


## Prerequisites

Before you begin, ensure you have met the following requirements:

- [Python 3.10.x](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/engine/install)

## Installation & Setup

### With Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Flow-Glow/Code-Jam-2023-Async-Aggrogaters.git
   cd Code-Jam-2023-Async-Aggrogaters
    ```
2. **Build the Docker image**
    ```bash
    docker build -t digital-shadows .
    ```

### Without Docker

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Flow-Glow/Code-Jam-2023-Async-Aggrogaters.git
   cd Code-Jam-2023-Async-Aggrogaters
    ```
2. **Install dependencies:**
    ```bash
    poetry install
    ```
## Running the Project

### With Docker

1. **Run the Docker container**
    ```bash
    docker run -it --rm digital-shadows
    ```

### Without Docker

1. Activate the poetry environment:
    ```bash
    poetry shell
    ```
2. Run the project:
    ```bash
    python main.py
    ```
## Contributing to the Project
1. Fork the project
2. Create a new branch (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -am 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.

## License
MIT License

Copyright (c) 2023 Joshua Fleshman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributors:
```
Joshua Fleshman(ChronosFU)
Leo Kim(leo.the.lion)
Daniel Febles(dfebs)
Ziv Landau(flowglow)
Avongard
Amor Budiyanto (sardines)
```
