#!/usr/bin/env python3
"""Basiid Authentication module"""
from api.v1.auth.auth import Auth
import base64
import binascii
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """BasicAuth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header method"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """returns the decoded value of a Base64 string
        base64_authorization_header"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decode = base64.b64decode(base64_authorization_header)
            return decode.decode('ascii')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """return tuple"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        new = decoded_base64_authorization_header.replace(":", ' ', 1)
        return tuple(new.split(" "))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            item = {"email": user_email}
            attr = User.search(item)
            if not attr:
                return None
            if len(attr) < 0:
                return None
            if not attr[0].is_valid_password(user_pwd):
                return None
            return attr[0]
        except KeyError:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """return current user"""
        header = self.authorization_header(request)
        print(header)
        extract = self.extract_base64_authorization_header(header)
        print(extract)
        decode = self.decode_base64_authorization_header(extract)
        print(decode)
        user_credentials = self.extract_user_credentials(decode)
        print(user_credentials[0], user_credentials[1])
        return self.user_object_from_credentials(user_credentials[0],
                                                 user_credentials[1])
