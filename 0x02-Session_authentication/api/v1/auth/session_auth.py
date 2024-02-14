#!/usr/bin/env python3
'''SessionAuth module'''
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    '''class SessionAuth that inherits from Auth'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """instance that creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        key = str(uuid.uuid4())
        self.user_id_by_session_id[key] = user_id
        return key

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        print('user id session', isinstance(session_id, str))
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """returns a User instance based on a cookie value"""
        cookie = self.session_cookie(request)
        print(cookie)
        print('Dic', self.user_id_by_session_id)
        return User.get(self.user_id_for_session_id(cookie))
