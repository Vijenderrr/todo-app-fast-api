from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

class Users(Base):
    __tablename__ = 'users' # This line defines the name of the table in the database that will be used to store user information. The table will be named 'users'.

    id = Column(Integer, primary_key = True, index = True) # This line defines a column named 'id' in the 'users' table. The column is of type Integer, it is the primary key of the table, and it is indexed for faster querying.

    username = Column(String, unique = True, index = True) # This line defines a column named 'username' in the 'users' table. The column is of type String, it must be unique (no two users can have the same username), and it is indexed for faster querying.

    email = Column(String, unique = True, index = True) # This line defines a column named 'email' in the 'users' table. The column is of type String, it must be unique (no two users can have the same email), and it is indexed for faster querying.

    first_name = Column(String, index = True) # This line defines a column named 'first_name' in the 'users' table. The column is of type String and it is indexed for faster querying.

    last_name = Column(String, index = True) # This line defines a column named 'last_name' in the 'users' table. The column is of type String and it is indexed for faster querying.

    hashed_password = Column(String) # This line defines a column named 'hashed_password' in the 'users' table. The column is of type String and it will be used to store the hashed version of the user's password for security purposes.

    is_active = Column(Boolean, default=True) # This line defines a column named 'is_active' in the 'users' table. The column is of type Boolean and it has a default value of True, indicating that a user is active by default.

    role = Column(String, default='user') # This line defines a column named 'role' in the 'users' table. The column is of type String and it has a default value of 'user', indicating that a user will have the role of 'user' by default unless specified otherwise.

    phone_number = Column(String, index=True) # This line defines a column for the user's phone number.

class Todos(Base):
    __tablename__= 'todos'  # This line defines the name of the table in the database that will be used to store the todo items. The table will be named 'todos'.
    
    id = Column(Integer, primary_key = True, index = True)  # This line defines a column named 'id' in the 'todos' table. The column is of type Integer, it is the primary key of the table, and it is indexed for faster querying.

    title = Column(String, index = True) # This line defines a column named 'title' in the 'todos' table. The column is of type String and it is indexed for faster querying.
    
    description = Column(String, index = True) # This line defines a column named 'description' in the 'todos' table. The column is of type String and it is indexed for faster querying.

    priority = Column(Integer, index = True) # This line defines a column named 'priority' in the 'todos' table. The column is of type Integer and it is indexed for faster querying.

    completed = Column(Boolean, default=False) # This line defines a column named 'completed' in the 'todos' table. The column is of type Boolean and it has a default value of False, indicating that a todo item is not completed by default.

    owner_id = Column(Integer, ForeignKey('users.id')) # This line defines a column named 'owner_id' in the 'todos' table. The column is of type Integer and it will be used to store the ID of the user who owns the todo item, allowing for a relationship between the 'todos' and 'users' tables.
