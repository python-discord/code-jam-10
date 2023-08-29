# (Modified) Python Discord Code Jam Repository Template

## Setting up for teammates - Tools

### flake8: general style rules

Our first and probably most important tool is flake8. It will run a set of plugins on your codebase and warn you about any non-conforming lines.
Here is a sample output:
```
~> flake8
./app.py:1:6: N802 function name 'helloWorld' should be lowercase
./app.py:1:16: E201 whitespace after '('
./app.py:2:1: D400 First line should end with a period
./app.py:2:1: D403 First word of the first line should be properly capitalized
./app.py:3:19: E225 missing whitespace around operator
```

Each line corresponds to an error. The first part is the file path, then the line number, and the column index.
Then comes the error code, a unique identifier of the error, and then a human-readable message.

If, for any reason, you do not wish to comply with this specific error on a specific line, you can add `# noqa: CODE` at the end of the line.
For example:
```python
def helloWorld():  # noqa: N802
    ...
```
will pass linting. Although we do not recommend ignoring errors unless you have a good reason to do so.

It is run by calling `flake8` in the project root.

### ISort: automatic import sorting

This second tool will sort your imports according to the [PEP8](https://www.python.org/dev/peps/pep-0008/#imports). That's it! One less thing for you to do!

It is run by calling `isort .` in the project root. Notice the dot at the end, it tells ISort to use the current directory.

### Pre-commit: run linting before committing

This third tool doesn't check your code, but rather makes sure that you actually *do* check it.

It makes use of a feature called [Git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) which allow you to run a piece of code before running `git commit`.
The good thing about it is that it will cancel your commit if the lint doesn't pass. You won't have to wait for Github Actions to report and have a second fix commit.

It is *installed* by running `pre-commit install` and can be run manually by calling only `pre-commit`.

[Lint before you push!](https://soundcloud.com/lemonsaurusrex/lint-before-you-push)

### Using the Default Pip Setup

Our default setup includes a bare requirement file to be used with a [virtual environment](https://docs.python.org/3/library/venv.html).

We recommend this if you never have used any other dependency manager, although if you have, feel free to switch to it. More on that below.

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

#### Installing the Dependencies
Once the environment is created and activated, use this command to install the development dependencies.
```shell
$ pip install -r dev-requirements.txt
```

#### Exiting the environment
Interestingly enough, it is the same for every platform
```shell
$ deactivate
```

Once the environment is activated, all the commands listed previously should work. We highly recommend that you run `pre-commit install` as soon as possible.
