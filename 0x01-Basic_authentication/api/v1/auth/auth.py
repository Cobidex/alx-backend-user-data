#!/usr/bin/env python3
"""
contains the auth class for authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    manages API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if endpoint requires auth
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if f"{path}/" in excluded_paths or path in excluded_paths:
            return False

        for pa in excluded_paths:
            if pa is None:
                continue
            elif pa.endswith('*'):
                if path.startswith(pa[:-1]):
                    return False
            elif f"{path}/" == pa or path == pa:
                return False
            else:
                return True

    def authorization_header(self, request=None) -> str:
        """
        handles authorization header
        """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Validates the current client """
        return None
