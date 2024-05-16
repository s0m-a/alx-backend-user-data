#!/usr/bin/env python3
"""
User passwords should NEVER be stored in plain text in a database
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed password, which is a byte string """
    encodes = password.encode()
    hashed = bcrypt.hashpw(encodes, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
     validate that the provided password matches the hashed password.
    """
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return valid
