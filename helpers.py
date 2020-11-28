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
        conn = sqlite3.connect('./baster_escuela.db')
        conn.row_factory = dict_factory  # Set dict factory
        db = conn.cursor()
        print("Connected to db")
        return db
    except Exception:
        print(Exception)


def write_blob_to_file(data, type, file_name):
    """Converts blob into img file and returns the name of the file created"""
    file_name_utf8 = strip_accents(file_name)
    filename = f"img/photos/{type}/{file_name_utf8}.jpg"
    with open(f".{url_for('static', filename=filename)}", "wb+") as file:
        file.write(data)
    return filename


def get_items(table, filters=[]):
    """Get records of a table, and, in case of having a photo column, write blob to file and get filename"""
    result_array = []
    db = connect_to_db()

    final_filter_string = 'WHERE '
    for i, _filter in enumerate(filters):
        field = _filter.get('field')
        values = _filter.get('values')
        values_str = ', '.join(values)
        filter_str = f"{field} IN ({values_str})"
        final_filter_string = final_filter_string + filter_str + (' AND ' if i < len(filters) - 1 else '')

    results = db.execute(f"SELECT * FROM {table} {final_filter_string if len(filters) > 0 else ''}").fetchall()

    for el in results:
        new_item = {}
        for key, value in el.items():
            if key == "foto":
                if value:
                    nombre = el['nombre'].replace(' ', '-')
                    apellido = f"{el['apellido'].replace(' ', '-')}"
                    file_name = f"{el['id']}-{nombre}-{apellido}"
                    complete_path = write_blob_to_file(
                        value, table, file_name)
                    new_item[key] = complete_path
                else:
                    new_item[key] = "img/logo.png"
            elif key == "mes":
                new_item[key] = month_number_to_text(value)
            else:
                new_item[key] = value

        result_array.append(new_item)

    return result_array


def month_number_to_text(month_number: int) -> str:
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    return months[month_number - 1]
