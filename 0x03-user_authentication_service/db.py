#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
from typing import Dict

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the db with the given email and hashed password.

        Args:
            email (str):user email
            hashed_password (str): user hashed password

        Returns:
            User: A User object representing the new user.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """Find a user with the specified attributes.

        Raises:
            error: NoResultFound: When no results are found.
            error: InvalidRequestError: When invalid query arguments are passed

        Returns:
            User: First row found in the `users` table.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Updates a user's attributes by user ID and arbitrary keyword
        arguments.

        Args:
            user_id (int): user ID.
            **kwargs: Keyword arguments representing the user's attributes to
            update.

        Raises:
            ValueError: If an invalid attribute is passed in kwargs.

        Returns:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User with id {} not found".format(user_id))

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("User has no attribute {}".format(key))
            setattr(user, key, value)

        try:
            self._session.commit()
        except InvalidRequestError:
            raise ValueError("Invalid request")
