#!/usr/bin/env python3
""" Base module
"""
from datetime import datetime
from typing import TypeVar, List, Iterable
from os import path
import json
import uuid

# Constants
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"  # Format for datetime serialization
DATA = {}  # In-memory storage for all objects


class Base:
    """ Base class for all models
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a Base instance.

        Args:
            args (list): Variable length argument list.
            kwargs (dict): Arbitrary keyword arguments.
        """
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))  # Unique identifier
        self.created_at = (
            datetime.strptime(kwargs.get('created_at'), TIMESTAMP_FORMAT)
            if kwargs.get('created_at') else datetime.utcnow()
        )
        self.updated_at = (
            datetime.strptime(kwargs.get('updated_at'), TIMESTAMP_FORMAT)
            if kwargs.get('updated_at') else datetime.utcnow()
        )

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """
        Check equality based on id.

        Args:
            other (Base): The other object to compare with.

        Returns:
            bool: True if both objects are the same, False otherwise.
        """
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """
        Convert the object to a JSON dictionary.

        Args:
            for_serialization (bool): Flag indicating
            if the conversion is for serialization.

        Returns:
            dict: JSON serializable dictionary of the object's attributes.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """
        Load all objects from a file into the in-memory storage.
        """
        s_class = cls.__name__
        file_path = ".db_{}.json".format(s_class)
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls):
        """
        Save all objects from the in-memory storage to a file.
        """
        s_class = cls.__name__
        file_path = ".db_{}.json".format(s_class)
        objs_json = {}
        for obj_id, obj in DATA[s_class].items():
            objs_json[obj_id] = obj.to_json(True)

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """
        Save the current object to the in-memory storage and file.
        """
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """
        Remove the current object from the in-memory storage and file.
        """
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """
        Count all objects of the class
        type in the in-memory storage.

        Returns:
            int: Number of objects in the storage.
        """
        s_class = cls.__name__
        return len(DATA[s_class].keys())

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """
        Return all objects of the class type.

        Returns:
            Iterable[Base]: List of all objects.
        """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> TypeVar('Base'):
        """
        Retrieve one object by its ID.

        Args:
            id (str): The unique identifier of the object.

        Returns:
            Base: The object with the given ID, or None if not found.
        """
        s_class = cls.__name__
        return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """
        Search for objects matching the given attributes.

        Args:
            attributes (dict): Dictionary of attributes to match.

        Returns:
            List[Base]: List of matching objects.
        """
        s_class = cls.__name__

        def _search(obj):
            """
            Helper function to determine if an
            object matches the search criteria.

            Args:
                obj (Base): The object to check.

            Returns:
                bool: True if the object matches, False otherwise.
            """
            if len(attributes) == 0:
                return True
            for k, v in attributes.items():
                if getattr(obj, k) != v:
                    return False
            return True
        return list(filter(_search, DATA[s_class].values()))
