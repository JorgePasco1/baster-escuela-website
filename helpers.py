from flask import url_for
import sqlite3
import unicodedata


# Define dictionary factory to be used for db results
def dict_factory(cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def strip_accents(text):
    text = unicodedata.normalize('NFD', text)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")

    return str(text)


def connect_to_db():
    try:
        conn = sqlite3.connect('./baster_escuela.db', check_same_thread=False)
        conn.row_factory = dict_factory  # Set dict factory
        db = conn.cursor()
        print("Success")
        return db
    except Exception:
        print(Exception)


def write_blob_to_file(data, type, file_name):
    """Convert blob into img file"""
    file_name_utf8 = strip_accents(file_name)
    filename = f"img/photos/{type}/{file_name_utf8}.jpg"
    print("filename", filename)
    with open(f".{url_for('static', filename=filename)}", "wb+") as file:
        file.write(data)
    return filename


def get_members(table):
    result_array = []
    db = connect_to_db()
    # No need to sanitize sql query, since it's gonna be used by admins
    results = db.execute(f"SELECT * FROM {table}").fetchall()

    for el in results:
        new_item = {}
        for key, value in el.items():
            if key != "foto":
                new_item[key] = value
            else:
                nombre = el['nombre'].replace(' ', '-')
                apellido = f"-{el['apellido'].replace(' ', '-')}"
                file_name = f"{nombre}{apellido}"
                complete_path = write_blob_to_file(
                    value, table, file_name)
                new_item[key] = complete_path
        result_array.append(new_item)

    return result_array
