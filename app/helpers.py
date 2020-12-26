""" Helper functions """

import os

import sqlite3
import unicodedata

from typing import List

from flask import url_for


def dict_factory(cursor, row):
    """ Define dictionary factory to be used for db results """
    # pylint: disable=invalid-name
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def strip_accents(text):
    """ Transform latin text into utf-8 """
    text = unicodedata.normalize('NFD', text)\
        .encode('ascii', 'ignore')\
        .decode("utf-8")

    return str(text)


def connect_to_db(db_name):
    """ Reusable function to connect to the database """
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = dict_factory  # Set dict factory
        database = conn.cursor()
        print("Connected to db")
        return database, conn
    except Exception:
        print(Exception)


def write_blob_to_file(data, _type, file_name):
    """Converts blob into img file and returns the name of the file created"""
    file_name_utf8 = strip_accents(file_name)
    filename = f"img/photos/{_type}/{file_name_utf8}.jpg"
    with open(f".{url_for('.static', filename=filename)}", "wb+") as file:
        file.write(data)
    return filename


def create_filters_string(filters):
    """ Create a sql filter string from a list of filters """
    if not filters:
        return ''

    final_filter_string = 'WHERE '
    for i, _filter in enumerate(filters):
        field = _filter.get('field')
        values = _filter.get('values')
        values_str = ', '.join(values)
        filter_str = f"{field} IN ({values_str})"
        final_filter_string = final_filter_string + \
            filter_str + (' AND ' if i < len(filters) - 1 else '')

    return final_filter_string


def create_fields_string(fields):
    """ Create a sql fields string from a list of fields """
    if not fields:
        return "*"

    return ",".join(fields)


def transform_result_value(key, value):
    """ Get the results of the query ready to be returned """
    if key == "id":
        return str(value)
    if key == "mes":
        return month_number_to_text(value)
    if key == "puesto":
        return "Oro" if value == 1 else "Plata" if value == 2 else "Bronce" if value == 3 \
            else None if not value else value

    return value


def group_results(results, group_by):
    """ Grou results by an specified key """
    keys = {el.get(group_by) for el in results}
    grouped_results = {}
    for key in keys:
        results_by_key = [el for el in results if el.get(group_by) == key]
        grouped_results[str(key)] = results_by_key

    return grouped_results


def transform_values(values_dict):
    """ Transform values from db to be sent to fe """
    result = {}
    for key, value in values_dict.items():
        value = value.strip()
        if key == 'puesto':
            mapper = {
                'oro': 1,
                'plata': 2,
                'bronce': 3
            }
            result[key] = mapper.get(value.lower()) or value
        else:
            result[key] = value
    return result


def get_items(table, db_name, filters=None, group_by=None, fields=None):
    """Get records of a table, and, in case of having a photo column, write blob to file and
    get filename"""
    result_array = []
    database, _ = connect_to_db(db_name)

    fields_string = create_fields_string(fields)
    filter_string = create_filters_string(filters)

    results = database.execute(
        f"SELECT {fields_string} FROM {table} {filter_string}").fetchall()

    for element in results:
        new_item = {}
        for key, value in element.items():
            new_item[key] = transform_result_value(key, value)

        result_array.append(new_item)

    if group_by and len(result_array) > 0:
        result_array = group_results(result_array, group_by)

    return result_array


# TODO: validate fields, return
def add_new_item_to_db(table, db_name, values_dict):
    """ Insert a new record to a db table """
    database, conn = connect_to_db(db_name)

    transformed_values = transform_values(values_dict)

    fields_string = ','.join(transformed_values.keys())
    values_placeholder = ('?,' * len(transformed_values))[:-1]
    values = tuple(transformed_values.values())

    database.execute(f''' INSERT INTO {table}({fields_string})
              VALUES({values_placeholder}) ''', values)

    conn.commit()


def month_number_to_text(month_number: int) -> str:
    """ get month text from number """
    months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
              'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    return months[month_number - 1]


def format_logros(logros: List[dict]) -> List[dict]:
    """ Format logros """
    logros_formatted = logros

    # Order by year
    for alumno_id, _logros in logros_formatted.items():
        logros_formatted[alumno_id] = sorted(
            _logros, key=lambda x: x['año'], reverse=True)

    return logros_formatted


def check_allowed_file(filename):
    """ Check if file has an allowed format """
    allowed_extensions = ['png', 'jpeg', 'jpg', 'heic']
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_file_to_multiple_directories(_file, filename, directories):
    """ Save a file in multiple directories """
    for directory in directories:
        if not os.path.isdir(directory):
            os.mkdir(directory)

        filepath = os.path.join(directory, filename)
        _file.save(filepath)
        _file.stream.seek(0)
