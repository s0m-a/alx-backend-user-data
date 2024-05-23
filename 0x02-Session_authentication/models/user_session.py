#!/usr/bin/env python3
"""
This is a userSession module
"""
from models.base import Base


class UserSession(Base):
    """
    This is a userSession class
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a UserSession instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
