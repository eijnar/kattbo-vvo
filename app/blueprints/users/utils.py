import hashlib
from PIL import Image, UnidentifiedImageError
from flask import current_app
import hashlib
import os
from PIL import Image

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

    picture_fn = image_hash + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile_pictures', picture_fn)

    try:
        with Image.open(form_picture) as image:
            image.thumbnail(output_size)
            image.save(picture_path)
            current_app.logger.info(f"Saved a new profile picture")
    except UnidentifiedImageError:
        raise ValueError("Invalid image file")

    return picture_fn