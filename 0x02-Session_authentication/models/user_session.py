#!/usr/bin/env python3
""" contains the UserSession model class definition """
from models.base import Base


class UserSession(Base):
    """ stores session ID in database """
    def __init__(self, *args: list, **kwargs: dict):
        """ initializes object fields """
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
