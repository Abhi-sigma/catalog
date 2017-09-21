import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import database_helpers as dh

Base = declarative_base()


class Catalog(Base):
    """schema for the table catalog """
    __tablename__ = 'catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    image = Column(String(250))
    creator = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref='catalog')

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class User(Base):
    """schema for the table user"""
    __tablename__ = 'users'
    name = Column(String(250))
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    picture = Column(String(250))


class Catalog_Item(Base):
    """schema for the table catalog items"""
    __tablename__ = 'catalog_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    image = Column(String(250))
    created_date = Column(DateTime, default=dh._get_date)
    creator = Column(Integer, ForeignKey('users.id'))
    catalog_relation = Column(Integer, ForeignKey('catalog.id'))
    catalog = relationship(Catalog, backref='catalog_item')
    user = relationship(User, backref='catalog_item')

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'catalog': self.catalog.name
        }

# creates the engine and tables if not already pressent
engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
