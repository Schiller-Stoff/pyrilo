# Pyrilo

CLI tool that ingests local bag files against gams5 

# Quickstart

### Usage

```sh
# cd into project root directory
pyrilo # check commands provided by pyrilo

# main command: syncs gams data with local bag files. (only one way folder --> GAMS5)
pyrilo ingest hsa

# check cli.py for additional arguments etc.


```

## Installation

Via python uv

1. Install uv on your machine basics section
2. Run `uv sync` in the root directory of this project
3. Activate uv generated .venv via `source .venv/bin/activate` (for linux) or `.venv\Scripts\activate` (for windows)
4. Run `pyrilo` to start the application


# External Dependencies

- available GAMS5 instance (e.g. via docker-compose.yml)