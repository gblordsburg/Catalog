import os
import sys
import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, session
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context


Base = declarative_base()


# User class taken from github repo udacity/APIs/Lesson_4/02_Adding Users
# and Logins/models.py used in the Fullstack Nanodegree-The Backend:
# Databases & Applications-Lesson 17 Securing your API.
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))
    email = Column(String(250))
    picture = Column(String(250))

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'email': self.email
        }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), primary_key=True, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'name': self.name,
        }


class Item(Base):
    __tablename__ = 'item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(1000))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    # Looks in category table and retrieves the name#
    category_name = Column(String, ForeignKey('category.name'))
    # variable category is the relationship between the class Relationship
    category = relationship(Category)

    @property
    def serialize(self):
        # Returns object data in easily serializable format
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
        }


engine = create_engine('sqlite:///catalog2.db')

Base.metadata.create_all(engine)
