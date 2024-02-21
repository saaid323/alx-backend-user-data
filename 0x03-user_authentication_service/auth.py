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
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        '''Creates session id'''
        info = {'email': email}
        try:
            user = self._db.find_user_by(**info)
        except (NoResultFound, InvalidRequestError):
            return
        setattr(user, 'session_id', _generate_uuid())
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        '''get user from session id'''
        info = {'session_id': session_id}
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(**info)
        except (NoResultFound, InvalidRequestError):
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        '''destroy session'''
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        '''reset password token'''
        info = {'email': email}
        try:
            user = self._db.find_user_by(**info)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        '''update password'''
        reset = {'reset_token': reset_roken}
        try:
            user = self._db.find_user_by(**reset)
        except (NoResultFound, InvalidRequestError):
            raise ValueError
        password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=password)
        self._db.update_user(user.id, reset_token=None)
