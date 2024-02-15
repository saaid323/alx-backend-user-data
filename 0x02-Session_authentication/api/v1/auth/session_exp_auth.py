#!/usr/bin/env python3
"""session expiration"""
from .session_auth import SessionAuth
import os
from flask import request
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self):
        """initialize"""
        super().__init__()
        self.session_duration = int(os.getenv('SESSION_DURATION'))
        if self.session_duration is None:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create session id using user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {'user_id': user_id, 'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = {'session dictionary': session_dictionary}
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """create duration for session id using created_at"""
        if session_id is None:
            return None
        if self.user_id_by_session_id.get(session_id) is None:
            return None
        dic = self.user_id_by_session_id.get(session_id).get('session dictionary')
        if self.session_duration <= 0:
            return dic.get('user_id')
        if dic.get('created_at') is None:
            return None
        time = dic.get('created_at') + timedelta(seconds=self.session_duration)
        if time < datetime.now():
            return None
        return dic.get('user_id')
