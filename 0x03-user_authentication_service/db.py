#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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
        '''add user to users table'''
        try:
            user = User(email=email, hashed_password=hashed_password)
            session = self._session
            session.add(user)
            session.commit()
        except IntegrityError:
            session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs):
        '''find user in users table'''
        session = self._session
        for k in kwargs.keys():
            if not hasattr(User, k):
                raise InvalidRequestError
        all = session.query(User).filter_by(**kwargs).first()
        if all is None:
            raise NoResultFound
        return all
