## How to setup the repository

```bash
$ python -m venv venv
$ source ./venv/bin/activate
```
If you want to contribute for the project, also do:
```bash
$ pip install -r requirements-dev.txt
$ pre-commit install
```

If you just want to run the game, do:
```bash
$ pip install -r requirements.txt
```

## How to run

```bash
$ export PYTHONPATH=$PYTHONPATH:$(pwd)
$ source ./venv/bin/activate
$ python ricochet_robots
```
