import random
import string
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token
from app import db
from app.utils.models import ShortLink

class URLShortener:
    """
    A utility class for shortening URLs with the option to embed JWT tokens.
    
    Keyword arguments:
    base_url -- The base URL for the shortened link
    registration_route -- The route to which the shortened link corresponds
    Return: Shortened URL.
    """

    def __init__(self, base_url, registration_route='/register'):
        self.base_url = base_url
        self.registration_route = registration_route

    def _generate_short_code(self, num_chars=6):
        """Generates a random short code for the URL."""
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(num_chars))

    def _is_unique(self, short_code):
        """Checks if the generated short code is unique."""
        return not ShortLink.query.filter_by(short_code=short_code).first()

    def _generate_jwt_token(self, identity, expires_at=None):
        """Generates a JWT token using Flask-JWT-Extended."""
        if expires_at is not None:
            expires_delta = timedelta(seconds=3600)#expires_at - datetime.utcnow()
            return create_access_token(identity=identity, expires_delta=expires_delta)
        else:
            # Fallback to a default expiration time if none provided
            expires_delta = timedelta(seconds=3600)  # 1 hour, for example
            return create_access_token(identity=identity, expires_delta=expires_delta)

    def create_short_link_with_jwt(self, identity, expires_at=3600):
        """Creates a shortened link embedding a JWT token."""
        jwt_token = self._generate_jwt_token(identity, expires_at)
        short_code = self._generate_short_code()
        
        # Ensure the generated short code is unique
        while not self._is_unique(short_code):
            short_code = self._generate_short_code()
        
        # Here you would typically save these details to your database
        short_link = ShortLink(
            original_url=f"{self.base_url}{self.registration_route}?token={jwt_token}",
            short_code=short_code,
            expires_at=datetime.utcnow() + timedelta(seconds=3600)
            #expires_at=expires_at if expires_at is not None else datetime.utcnow() + timedelta(seconds=3600)
        )
        db.session.add(short_link)
        db.session.commit()

        return f"{self.base_url}/{short_code}"

    def get_original_url(self, short_code):
        """Retrieves the original URL from a short code."""
        link = ShortLink.query.filter_by(short_code=short_code).first()
        if link and link.expires_at > datetime.utcnow():
            return link.original_url
        return None
