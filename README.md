# Python Discord Code Jam Repository

[![Tests](https://github.com/smileyface12349/itinerant-iterators/actions/workflows/tests.yaml/badge.svg)](https://github.com/smileyface12349/itinerant-iterators/actions/workflows/tests.yaml)
[![Lint](https://github.com/smileyface12349/itinerant-iterators/actions/workflows/lint.yaml/badge.svg)](https://github.com/smileyface12349/itinerant-iterators/actions/workflows/lint.yaml)

#### Creating the environment
Create a virtual environment in the folder `.venv`.
```shell
$ python -m venv .venv
```

#### Enter the environment
It will change based on your operating system and shell.
```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

#### Install Dependencies
- Dependencies required to run the application: `$ pip install -r requirements.txt`

- Dependencies required to develop and run tests: `$ pip install -r dev-requirements.txt`

#### Running Tests
`$ pytest`

#### Run the Application
```shell
# run the UI
$ python3 -m app ui
# run the CLI
$ python3 -m app cli <options> <args>
```

#### Example CLI
```shell
# watermark
python3 -m app cli watermark encode "secret message" data/image.jpg data/encoded_image.png
python3 -m app cli watermark decode data/encoded_image.png
secret message

# obfuscate
python3 -m app cli obfuscate data/image.jpg data/output.jpg --regex "\d+" --mode blur
python3 -m app cli obfuscate data/image.jpg data/output.jpg "hide this text" "other text" --mode blur
python3 -m app cli obfuscate data/image.jpg data/output.jpg "hide this text" "other text" --mode colour --colour red
```
