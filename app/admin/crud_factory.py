""" Factory methods for crud operations """

import os

from app.common.constants import BASE_ADMIN_STATIC_URL, BASE_PUBLIC_STATIC_URL
from app.common.file_system import check_allowed_file, save_file_to_multiple_directories
from app.common.database import update_record_in_db, delete_record_in_db, add_new_item_to_db


variable_name_dict = {
    'entrenadores': 'ENTRENADORES',
    'atletas': 'ATLETAS'
}


def update_one(database, _type, request, _id):
    """ Update one record in the database """
    try:
        variable_name = variable_name_dict.get(_type)

        public_upload_folder = BASE_PUBLIC_STATIC_URL + (os.environ.get(
            f'{variable_name}_UPLOAD_FOLDER') or 'img/photos/')
        admin_upload_folder = BASE_ADMIN_STATIC_URL + (os.environ.get(
            f'{variable_name}_UPLOAD_FOLDER') or 'img/photos/')

        _file = request.files['file']
        row_info = dict(request.form)
        filename = None

        if _file and check_allowed_file(_file.filename):
            extension = _file.filename.rsplit('.', 1)[1].lower()
            filename = f"{_type}-{_id}.{extension}"

            save_file_to_multiple_directories(
                _file, filename, [public_upload_folder, admin_upload_folder])

            row_info['foto'] = f"{public_upload_folder.split('static/')[1]}/{filename}"

        update_record_in_db(_type, database,
                            row_info, {'id': _id})

        return True
    except Exception as excep:
        print(excep)
        return False


def delete_one(database, _type, _id):
    """ Delete one row from the database table by id """

    try:
        delete_record_in_db(_type, database, {'id': _id})
        return True
    except Exception as excep:
        print(excep)
        return False


def add_one(database, _type, request):
    """ Add one record to the database """
    try:
        inserted_row_id = add_new_item_to_db(
            _type, database, request.form)

        variable_name = variable_name_dict.get(_type)

        public_upload_folder = BASE_PUBLIC_STATIC_URL + (os.environ.get(
            f'{variable_name}_UPLOAD_FOLDER') or 'img/photos/')
        admin_upload_folder = BASE_ADMIN_STATIC_URL + (os.environ.get(
            f'{variable_name}_UPLOAD_FOLDER') or 'img/photos/')

        _file = request.files['file']
        filename = None

        if _file and check_allowed_file(_file.filename):
            extension = _file.filename.rsplit('.', 1)[1].lower()
            filename = f"{_type}-{inserted_row_id}.{extension}"

            save_file_to_multiple_directories(
                _file, filename, [public_upload_folder, admin_upload_folder])

            info = {
                "foto": f"{public_upload_folder.split('static/')[1]}/{filename}"}

            update_record_in_db(_type, database,
                                info, {'id': inserted_row_id})

        return True
    except Exception as excep:
        print(excep)
        return False
