#!/usr/bin/env python3
"""Module to manage the API authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def check_slash(self, path: str, excluded_paths: List[str]) -> bool:
        '''handles the slash'''
        for i in excluded_paths:
            i = i[:-1] if i[-1] is '/' else i
            if i == path:
                return False
        return True

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """return false if path or excluded_paths is none or path is not in
        excluded_paths"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path = path[:-1] if path[-1] is '/' else path
        if self.check_slash(path, excluded_paths):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """check is there is Authorization key in request"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None"""
        if request is None:
            return None
