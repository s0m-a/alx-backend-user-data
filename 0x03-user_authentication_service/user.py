#!/usr/bin/env python3
"""Module for Users.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
