#!/usr/bin/env python3
""" contains the SessionDBAuth class """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ Authentication system to store session ID to database """
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession
        and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kwargs = {"user_id": user_id, "session_id": session_id}
        user_session = UserSession(**kwargs)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        returns the User ID by requesting UserSession in the
        database based on session_id
        """
        if not session_id:
            return None
        UserSession.load_from_file()
        session_ids = UserSession.search({'session_id': session_id})
        if not session_ids:
            return None
        if datetime.utcnow() > session_ids[0].created_at + timedelta(
          seconds=self.session_duration):
            return None
        return session_ids[0].user_id

    def destroy_session(self, request=None):
        """
        destroys the UserSession based on the Session ID from
        the request cookie
        """
        session_id = request.cookies.get('session_id')
        if not session_id:
            return None
        UserSession.load_from_file()
        session_ids = UserSession.search({'session_id': session_id})
        if not session_ids:
            return None
        session_ids[0].remove()
        UserSession.save_to_file()
