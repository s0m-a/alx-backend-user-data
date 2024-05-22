#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to manage the API authentication """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ For validating if endpoint requires auth """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        lenPath = len(path)
        if lenPath == 0:
            return True

        slash = True if path[lenPath - 1] == '/' else False

        tmpPath = path
        if not slash:
            tmpPath += '/'

        for x in excluded_paths:
            lenExc = len(x)
            if lenExc == 0:
                continue

            if x[lenExc - 1] != '*':
                if tmpPath == x:
                    return False
            else:
                if x[:-1] == path[:lenExc - 1]:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ A method that handles authorization header """
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ Validates current user """
        return None