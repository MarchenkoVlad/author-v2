from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

PWD = 'password'
USR= 'root'

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" #'mysql://{}:{}@localhost:3306/mydatabase'.format(USR, PWD)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()
#функция, которая создает базовый класс
# для декларативных определений классовdb