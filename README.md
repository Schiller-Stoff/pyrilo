# Pyrilo

prototypical python based gams5 client application - as proxy against the REST-API.

imitates the behavior of Cirilo in Python.

# Quickstart

## Deployment / usage

Via python rye

1. Install rye on your machine (https://rye.astral.sh/guide/installation/) and read through rye basics section
2. Run `rye sync` in the root directory of this project
3. Activate rye generated .venv via `source .venv/bin/activate` (for linux) or `.venv\Scripts\activate` (for windows)
4. Run `pyrilo` to start the application


# External Dependencies

- available GAMS5 instance (e.g. via docker-compose.yml)