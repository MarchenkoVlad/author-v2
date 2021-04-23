from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, Enum
from crypt import bcrypt
from db import Base
from datetime import datetime
from sqlalchemy.types import Text
from flask_login import UserMixin

class User(UserMixin, Base):
    '''
    Base model User
    '''

    __tablename__ = 'Users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(2000))

    def __init__(self, first_name, last_name,email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
    
    def get_id(self):
        return str(self.user_id)


class Article(Base):

    __tablename__ = 'Articles'

    article_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    intro = Column(String(300), nullable=False)
    article_text = Column(Text, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)


    def __init__(self, title, intro ,article_text):
        self.title = title
        self.intro = intro
        self.article_text = article_text
        
        
    def __repr__(self):
        return '<Article %r' % self.article_id


