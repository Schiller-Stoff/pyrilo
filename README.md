# Pyrilo

prototypical python based gams5 client application - as proxy against the REST-API.

imitates the behavior of Cirilo in Python.

(work in progress)

# Quickstart

## Deployment / usage

1. Standard python venv workflow (initialize local venv, install from requirements.txt)
2. Run gams6-client/main.py


## Additional

- Download model fromm here: https://fasttext.cc/docs/en/crawl-vectors.html ('cc.en.300.bin') and paste + unzip it into ./models
- Start venv via linux / wsl "source ./venv/bin/activate"
- Install dependencies from requirements.txt (you might also have to install python-wheel on your machine to use fasttext)
- Run ./scripts/fasttext_scale_down.py --> Reduce the model size to 'cc.en.20.bin' https://fasttext.cc/docs/en/crawl-vectors.html#:~:text=The%20pre%2Dtrained%20word%20vectors,can%20use%20our%20dimension%20reducer.
- Run main.py


# Dependencies

- available GAMS5 instance.
- python 3.12