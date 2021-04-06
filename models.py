from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Enum
from crypt import bcrypt
from db import Base

class User(Base):
    '''
    Base model User
    '''

    __tablename__ = 'Users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    login = Column(String(50), unique=True)
    password = Column(String(2000))

    def __init__(self, first_name, last_name,email,login, password):
       # self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.login = login
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
