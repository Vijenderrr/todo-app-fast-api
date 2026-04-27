from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'  # This line defines the URL for the SQLite database, where 'sqlite:///' indicates that it is a SQLite database and './todo.db' specifies the location and name of the database file.

# For PostgreSQL, the URL format is: 'postgresql://user:password@localhost/dbname'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:pa%24%24word@localhost/TodoApplicationDatabase'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})  # This line creates a SQLAlchemy engine using the specified database URL. The connect_args parameter is used to pass additional arguments to the database connection, and in this case, it is set to {"check_same_thread": False} to allow multiple threads to access the database.

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # This line creates a SQLAlchemy engine using the specified database URL. The engine is responsible for managing the database connection and executing SQL statements.

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)  # This line creates a sessionmaker object that will be used to create database sessions. The autocommit parameter is set to False to disable automatic commits, the autoflush parameter is set to False to disable automatic flushing of changes to the database, and the bind parameter is set to the engine created in the previous line to specify the database connection.

Base = declarative_base()  # This line creates a base class for the database models using the declarative_base function from SQLAlchemy. This base class will be used to define the database models for the application.

