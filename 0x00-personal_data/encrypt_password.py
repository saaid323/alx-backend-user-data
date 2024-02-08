#!/usr/bin/env python3
'''encrypt_password.py file'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''function that expects one string argument name password
    and returns a salted, hashed password, '''
    password = password.encode('utf-8')
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return hash
