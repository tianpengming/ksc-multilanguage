from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import configs

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.\
                       format(configs['db']['name'],configs['db']['password'],\
                              configs['db']['ip'],configs['db']['port'],configs['db']['database']))
DBSession = sessionmaker(bind=engine)
