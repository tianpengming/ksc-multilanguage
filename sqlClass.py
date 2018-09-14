from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Application(Base):
    # 表的名字:
    __tablename__ = 'application'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    identification = Column(String(20))
    name = Column(String(20))
    description = Column(String(20))
    translation = relationship("Translation", backref="application")


class Character(Base):
    # 表的名字:
    __tablename__ = 'character'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(String(20))
    translation = relationship("Translation", backref="character")



class Language(Base):
    # 表的名字:
    __tablename__ = 'language'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    identification = Column(String(20))
    name = Column(String(20))
    description = Column(String(20))
    translation = relationship("Translation", backref="language")


class Translation(Base):
    # 表的名字:
    __tablename__ = 'translation'
    # 表的结构:
    id = Column(Integer, primary_key=True)
    language_id = Column(Integer, ForeignKey("language.id"))
    application_id = Column(Integer, ForeignKey("application.id"))
    character_id = Column(Integer, ForeignKey("character.id"))
    cha_translation = Column(String(20))
