from flask import Blueprint, redirect, current_app

utils = Blueprint('utils', '__name__')

@utils.route('/<short_code>')
def redirect_to_original_url(short_code):
    urlshortener = current_app.urlshortener
    original_url = urlshortener.get_original_url(short_code)

    if original_url is not None:
        return redirect(original_url)
    else:
        return 'URL not found', 404