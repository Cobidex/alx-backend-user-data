#!/usr/bin/env python3
"""authentication methods
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """returns byte form of password
    """
    password = password.encode("utf-8")
    return bcrypt.hashpw(password, bcrypt.gensalt())


def _generate_uuid() -> str:
    """generates a uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password = _hash_password(password)
            user = self._db.add_user(email, password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """validates a users credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode("utf-8")

            if bcrypt.checkpw(password, user.hashed_password):
                return True
            return False

        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """creates a session id for a user
        """
        try:
            user = self._db.find_user_by(email=email)
            user.session_id = _generate_uuid()
            return user.session_id
        except NoResultFound:
            return None
