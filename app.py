from flask import Flask, render_template, url_for
import sqlite3

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Define dictionary factory to be used for db results
def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


# Connecting to db
try:
    conn = sqlite3.connect('./baster_escuela.db', check_same_thread=False)
    conn.row_factory = dict_factory  # Set dict factory
    db = conn.cursor()
    print("Success")
except Exception:
    print(Exception)


def write_blob_to_file(data, type, file_name):
    """Convert blob into img file"""
    filename = f"img/photos/{type}/{file_name}.jpg"
    with open(f".{url_for('static', filename=filename)}", "wb+") as file:
        file.write(data)
    return filename


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/about')
def about():
    name = 'about'
    directiva = db.execute("SELECT * FROM miembros_directiva").fetchall()
    directiva_info = []

    for el in directiva:
        new_item = {}
        for key, value in el.items():
            if key != "foto":
                new_item[key] = value
            else:
                file_name = f"{el['id']}-{el['nombre']}-{el['apellido']}"
                complete_path = write_blob_to_file(
                    value, "directiva", file_name)
                new_item[key] = complete_path
        directiva_info.append(new_item)

    print("directiva_info", directiva_info)
    return render_template(f"{name}.html", active=f"{name}", directiva=directiva_info)


@app.route('/atletas')
def atletas():
    name = 'atletas'
    return render_template(f"{name}.html", active=f"{name}")


@app.route('/abierto')
def abierto():
    name = 'abierto'
    return render_template(f"{name}.html", active=f"{name}")


@app.route('/productos')
def productos():
    name = 'productos'
    return render_template(f"{name}.html", active=f"{name}")
