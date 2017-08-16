#from sqlalchemy import Column, String, create_engine
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *

#创建数据表
engine = None
def connect_mysql():
    global engine
    engine = create_engine('mysql+mysqlconnector://root:123456@localhost:3306/multiLanguage')
    metadata = MetaData(engine)
    language = Table('language', metadata,
        Column('id', Integer, primary_key = True),
        Column('name', String(20)))
#创建数据表，如果数据表存在则忽视！！！
    metadata.create_all(engine)
#获取数据库链接，以备后面使用！！！！！
    conn = engine.connect()