#!/usr/bin/env python3
'''encryption module'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    '''hashes password'''
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''register user'''
        try:
            info = {'email': email}
            user = self._db.find_user_by(**info)
        except NoResultFound:
            password = _hash_password(password)
            new_user = self._db.add_user(email, password)
            return new_user
        if user is not None:
            raise ValueError(f"User {user.email} already exists")
