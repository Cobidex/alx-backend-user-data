#!/usr/bin/env python3
"""
contains the SessionAuth class
"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """ implements a session based authentication """
    user_id_by_session_id: dict = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        u_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[u_id] = user_id
        return u_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns a User instance based on a cookie value
        """
        s_id: str = self.session_cookie(request)
        u_id: str = self.user_id_for_session_id(s_id)
        user: TypeVar('User') = User.get(u_id)

        return user
