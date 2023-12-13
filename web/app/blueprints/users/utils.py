from pathlib import Path
import hashlib
from PIL import Image, UnidentifiedImageError
from flask import current_app
import hashlib
import os
from PIL import Image

from werkzeug.exceptions import BadRequest


class FileUploadHandler:
    def __init__(self, allowed_extensions, base_upload_folder, size=(125, 125)):
        self.allowed_extensions = allowed_extensions
        self.base_upload_folder = base_upload_folder
        self.size = size

    def save_file(self, file, is_public=False):
        if not self.is_allowed_extension(file.filename):
            raise BadRequest("Invalid file format")

        file_hash = self.generate_file_hash(file)
        relative_path = self.construct_relative_path(file_hash, file.filename, is_public)
        full_path = Path(self.base_upload_folder) / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        if self.is_image(file.filename):
            self.save_image(file, full_path)
        else:
            file.save(full_path)

        return str(relative_path)

    def is_allowed_extension(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        return ext in self.allowed_extensions

    def generate_file_hash(self, file):
        file.seek(0)
        return hashlib.blake2b(file.read(), digest_size=10).hexdigest()

    def construct_relative_path(self, file_hash, filename, is_public):
        privacy_folder = 'public' if is_public else 'private'
        dir_level1 = file_hash[:2]
        dir_level2 = file_hash[2:4]
        _, f_ext = os.path.splitext(filename)
        return Path(privacy_folder) / dir_level1 / dir_level2 / (file_hash + f_ext)

    def is_image(self, filename):
        return os.path.splitext(filename)[1].lower() in ['.jpg', '.jpeg', '.png']

    def save_image(self, file, path):
        try:
            with Image.open(file) as image:
                image.thumbnail(self.size)
                image.save(path)
        except Exception as e:
            raise BadRequest("Invalid image file: " + str(e))


# class FileUploadHandler:
#     def __init__(self, allowed_extensions, base_upload_folder, size=(125, 125)):
#         self.allowed_extensions = set(allowed_extensions)
#         self.base_upload_folder = base_upload_folder
#         self.size = size

#     def save_file(self, file):
#         if not self.is_allowed_extension(file.filename):
#             raise BadRequest("Filtyp ej tillåten")

#         file_hash = self.generate_file_hash(file)
#         relative_path = self.construct_relative_path(file_hash, file.filename)
#         full_path = Path(self.base_upload_folder) / relative_path
#         full_path.parent.mkdir(parents=True, exist_ok=True)

#         if self.is_image(file.filename):
#             self.save_image(file, full_path)
        
#         if self.is_document(file.filename):
#             self.save_document(file, full_path)

#         else:
#             file.save(file, full_path)

#         current_app.logger.info(f'{relative_path}')
#         return str(relative_path)

#     def is_allowed_extension(self, filename):
#         file_extension = os.path.splitext(filename)[1].lower()
#         return file_extension in self.allowed_extensions

#     def generate_file_hash(self, file):
#         file.seek(0)
#         return hashlib.blake2b(file.read(), digest_size=10).hexdigest()

#     def construct_relative_path(self, file_hash, filename, folder_name):
#         dir_level1 = file_hash[:2]
#         dir_level2 = file_hash[2:4]
#         _, f_ext = os.path.splitext(filename)
#         return Path(folder_name) / dir_level1 / dir_level2 / (file_hash + f_ext)

#     def is_image(self, filename):
#         file_extension = os.path.splitext(filename)[1].lower()
#         return file_extension in ['.jpg', '.jpeg', '.png']

#     def is_document(self, filename):
#         file_extension = os.path.splitext(filename)[1].lower()
#         return file_extension in ['.doc', '.docx', '.pdf', '.md']

#     def save_image(self, file, path):
#         try:
#             with Image.open(file) as image:
#                 image.thumbnail(self.size)
#                 image.save(path)
#                 return True
#         except UnidentifiedImageError:
#             raise BadRequest("Invalid image file")
#         except Exception as e:
#             raise BadRequest("Error saving image: " + str(e))
        
#     def save_document(self, file, path):
#         pass

def save_profile_picture_adv(form_picture, output_size=(125, 125)):
    """
    Save the profile picture to the server.

    Args:
        form_picture (FileStorage): The uploaded profile picture.
        output_size (tuple, optional): The desired output size of the image. Defaults to (125, 125).

    Returns:
        str: The filename of the saved picture.

    Raises:
        ValueError: If the file format is not allowed or if the image is invalid.
    """

    _, f_ext = os.path.splitext(form_picture.filename)
    allowed_extensions = ['.jpg', '.jpeg', '.png']
    if f_ext.lower() not in allowed_extensions:
        raise ValueError("Invalid file format")

    blake2b_hash = hashlib.blake2b(form_picture.read(), digest_size=10).hexdigest()
    image_hash = blake2b_hash

    dir_level1 = image_hash[:2]
    dir_level2 = image_hash[2:4]

    profile_picture_fullname = image_hash + f_ext
    profile_picture_save_folder = Path(current_app.config['UPLOAD_FOLDER']) / 'profile_pictures' / dir_level1 / dir_level2
    hash_folder = dir_level1 / dir_level2
    db_profile_picture = hash_folder / profile_picture_fullname
    save_picture = profile_picture_save_folder / profile_picture_fullname

    hash_folder.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(form_picture) as image:
            image.thumbnail(output_size)
            image.save(save_picture)
            current_app.logger.info(f"Saved a new profile picture")
    except UnidentifiedImageError:
        raise ValueError("Invalid image file")

    return db_profile_picture