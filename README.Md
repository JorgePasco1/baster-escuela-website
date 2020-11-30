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

### Subdomains

This app has a subdomain (admin), aimed at SuperUsers. If you want to test this functionality, you will need to do the following:

Setup new host in your hosts file (You can take a look at this [article](https://docs.rackspace.com/support/how-to/modify-your-hosts-file/) for some help with that). Example for this particular use case:

```bash
127.0.0.1	basterescuela.test
127.0.0.1	admin.basterescuela.test
```

Once this is set, you will need to create add the following to your .flaskenv file:

```bash
HOST='basterescuela.test:5000'
```

### Running app

Run the app by executing:

```bash
flask run
```

Optionally, the `FLASK_DEBUG=1` flag can be added prior to the command, to allow for updates on code change, without having to restart the server.
