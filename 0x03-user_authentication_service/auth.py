#!/usr/bin/env python3
'''encryption module'''
import bcrypt


def _hash_password(password: str) -> bytes:
    '''hashes password'''
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
