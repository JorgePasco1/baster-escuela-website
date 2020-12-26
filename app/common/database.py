""" Functions related to database """

import sqlite3

from app.common.helpers import group_results
from app.common.mappers import transform_result_value, transform_values


def dict_factory(cursor, row):
    """ Define dictionary factory to be used for db results """
    # pylint: disable=invalid-name
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


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

    inserted_row_id = database.lastrowid
    conn.commit()
    return inserted_row_id


def update_record_in_db(table, db_name, values_dict, item_identifier):
    """ Update an exisiting record in a db table """
    if not item_identifier:
        raise Exception('The request to update item needs an item identifier')

    database, conn = connect_to_db(db_name)
    transformed_values = transform_values(values_dict)

    transformation_string = ','.join(
        [f"{k}='{v}'" for k, v in transformed_values.items()])
    filter_string = ' AND '.join(
        [f"{k}={v}" for k, v in item_identifier.items()])

    print("transformation_string", transformation_string)
    print("filter_string", filter_string)

    database.execute(f''' UPDATE {table}
                SET {transformation_string}
                WHERE {filter_string}''')

    conn.commit()
