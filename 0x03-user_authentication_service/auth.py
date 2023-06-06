#!/usr/bin/env python3
"""authentication methods
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """returns byte form of password
    """
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt())
