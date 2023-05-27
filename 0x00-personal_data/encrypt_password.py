#!/usr/bin/env python3
'''
contains the hash_password function
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''
    hashes a passord string
    '''
    pwd = password.encode()
    hashed = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed
