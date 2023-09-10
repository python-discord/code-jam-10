# :=

This repository contains **The Top-level Walruses** team's submission for the [10th Python Discord Code Jam](https://www.pythondiscord.com/events/code-jams/10/).

TODO: This readme will be updated as needed during the development of the project.

## Setting up

This project requires Python 3.11 or newer to run.

## Usage

### Generating an image

Use the `generate` command to generate an image. The command can take input data either as a string or a path to a file.

```sh
python -m piet generate "My super secret message!" out.png
```

Besides input and output paths, the command also accepts the following options:

- `--cols`: Override the number of columns in the output image, by default the generator will automatically determine the best number of columns.
- `--recurse <depth>`: Generate images recursively, by default this is disabled. More on this later.
- `--input <text>`: Input to pass to the interpreter, used as a cipher shift. More on this later as well.
- `--step-limit`: Limit the number of steps the interpreter can take, by default this is 1 million. This is useful to prevent infinite loops.
- `--debug`: Enable debug mode, which will print out the state of the interpreter after each step.

### Interpreting an image

Running your newly generated image is rather straighforward:

```sh
python -m piet run out.png
```

This command has the same `--input`, `--step-limit` and `--debug` options as the `generate` command.
The additional `--execute` flag will try to execute the content of the image as Python code.

### Encrypting with a key

By passing a string to the `--input` option, you can encrypt your message with a key.

```sh
python -m piet generate "My super secret message!" out.png --input "my secret key"
```

Using a Vigenère cipher, the bytes in the input data will be shifted by the bytes in the key before being encoded into the image.
The catch is the reverse operation is encoded in the image as well, so you must pass the same key to the interpreter to decrypt the message.
If run without a key, the interpreter will fail to execute the program.

## Development

This project is built and tested with Python 3.11.

- Create a virtual environment and activate it: `python -m venv .venv`
- Install project dependencies: `pip install -r requirements.txt`
- Install development dependencies: `pip install -r requirements-dev.txt`
- Set up pre-commit hooks: `pre-commit install`
