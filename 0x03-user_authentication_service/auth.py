#!/usr/bin/env python3
'''encryption module'''
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    '''hashes password'''
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
        '''generate uuid'''
        uuid = uuid.uuid4()
        retrun str(uuid)


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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate the login"""
        info = {'email': email}
        try:
            user = self._db.find_user_by(**info)
        except (NoResultFound, InvalidRequestError):
            return False
        password = password.encode('utf-8')
        if bcrypt.checkpw(password, user.hashed_password):
            return True
        return False
