#!/usr/bin/env python3
"""
contains the class SessionExpAuth
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv


class SessionExpAuth(SessionAuth):
    """
    adds an experiation date to the authentication
    """
    def __init__(self):
        """ initializes the expiration time """
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """ return session id created """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {'user_id': user_id, 'created_at':datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ returns user_id for session dictionar """
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if not session_dictionary:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        if "created_at" not in session_dictionary:
            return None
        created_at = session_dictionary.get('created_at')
        expiration_time = timedelta(seconds=self.session_duration) + created_at
        if expiration_time < datetime.now():
            return None
        return session_dictionary.get("user_id")
