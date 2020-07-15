# Baster Escuela de Tenis de Mesa Website

Website build on Flask and sqlite.

## Instructions

### Virtual env

Creating a virtual environment is recommended to avoid overwriting global installs of this project's dependencies.

To create a virtual env, create a `venv` folder inside the project's directory, and activate it, as follows:

```bash
python3 -m venv venv
. venv/bin/activate
```

### Installing requirements

Then, install the requirements with:

```bash
pip install -r requirements.txt
```

### Running app

Run the app by executing:

```bash
flask run
```

Optionally, the `FLASK_DEBUG=1` flag can be added prior to the command, to allow for updates on code change, without having to restart the server.
