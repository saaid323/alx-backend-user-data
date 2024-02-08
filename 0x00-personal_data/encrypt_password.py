#!/usr/bin/env python3
'''encrypt_password.py file'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''function that expects one string argument name password
    and returns a salted, hashed password, '''
    password = password.encode('utf-8')
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return hash


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''function that expects 2 arguments and returns a boolean'''
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
