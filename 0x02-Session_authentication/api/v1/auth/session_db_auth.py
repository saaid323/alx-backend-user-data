#!/usr/bin/env python3
"""session auth db module"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """SessionDBAuth class"""

    def create_session(self, user_id=None):
        """create_session method"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        dic = {"user_id": user_id, 'session_id': session_id}
        user_session = UserSession(**dic)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user_id_for_session_id method"""
        s_id = UserSession.search({"session_id": session_id})
        if not s_id:
            return None
        if len(s_id) <= 0:
            return None
        created = s_id[0].created_at
        time = timedelta(seconds=self.session_duration) + created
        if time < datetime.now():
            return None
        return s_id[0].user_id

    def destroy_session(self, request=None) -> bool:
        """destroy_session method"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        s_id = UserSession.search({'session_id': session_id})
        if not s_id or len(s_id) <= 0:
            return False
        s_id[0].remove()
        return True
