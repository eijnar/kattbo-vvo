from pathlib import Path
import hashlib
from PIL import Image
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