import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, index=True)
    password = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.login})>"


class Products(Base):
    __tablename__ = 'Products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    size = Column(Integer, index=True)
    condition = Column(String, index=True)
    color = Column(String, index=True)
    location = Column(String, index=True)
    payment_method = Column(String, index=True)
    description = Column(String, index=True)
    



















