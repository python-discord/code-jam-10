# list available just commands
list:
    just --list

# run unit tests
test:
    pytest tests

# initialise development environment
init:
    python -m venv .venv
    source venv/bin/activate
    pip install -r dev-requirements.txt
    pip install -r requirements.txt
    pre-commit install

# format code
fmt: isort
    python -m black .

# sort imports
isort:
    isort .

# lint code
lint:
    flake8
