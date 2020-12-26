""" Functions related to file system """
import os


# def write_blob_to_file(data, _type, file_name):
#     """Converts blob into img file and returns the name of the file created"""
#     file_name_utf8 = strip_accents(file_name)
#     filename = f"img/photos/{_type}/{file_name_utf8}.jpg"
#     with open(f".{url_for('.static', filename=filename)}", "wb+") as file:
#         file.write(data)
#     return filename


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
