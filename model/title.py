from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.types import(
    Date,
    Boolean,
    Time,
    DateTime
)
from core.database import Base

from model.base import ModelBase
from datetime import datetime

class TitleData(ModelBase, Base):
    __tablename__ = 'title_data'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_title = Column(Integer)
    id_data_source = Column(Integer)
    data = Column(String(255))
    language = Column(String(255))
    quality = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def add(cls, session, id_title, id_data_source, data, language, quality):
        title_data = TitleData()
        title_data.id_title = id_title
        title_data.id_data_source = id_data_source
        title_data.data = data
        title_data.language = language
        title_data.quality = quality
        session.add(title_data)
        session.commit()
        session.refresh(title_data)
        return TitleData.find_by_id(session=session, id=title_data.id)

    @classmethod
    def find_by_title_id(cls, session, id_title):
        return session.query(
            cls.id,
            cls.id_title,
            cls.id_data_source,
            cls.data,
            cls.language,
            cls.quality,
            cls.date_created
        ).filter_by(id_title=id_title).all()


class TitleDataSubtitle(ModelBase, Base):
    __tablename__ = 'title_data_subtitle'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_title = Column(Integer)
    id_data_source = Column(Integer)
    data = Column(String(255))
    language = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def add(cls, session, id_title, id_data_source, data, language):
        title_data_subtitle = TitleDataSubtitle()
        title_data_subtitle.id_title = id_title
        title_data_subtitle.id_data_source = id_data_source
        title_data_subtitle.data = data
        title_data_subtitle.language = language
        session.add(title_data_subtitle)
        session.commit()
        session.refresh(title_data_subtitle)
        return TitleDataSubtitle.find_by_id(session=session, id=title_data_subtitle.id)


    @classmethod
    def find_by_title_id(cls, session, id_title):
        return session.query(
            cls.id,
            cls.id_title,
            cls.id_data_source,
            cls.data,
            cls.language,
            cls.date_created
        ).filter_by(id_title=id_title).all()





class TitleType(ModelBase, Base):
    __tablename__ = 'title_type'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255))
    key = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())
    @classmethod
    def list_all(cls, session):
        return session.query(
            cls.id,
            cls.description,
            cls.key,
            cls.date_created
        ).all()
    @classmethod
    def find_by_key(cls, session, key):
        return session.query(
            cls.id,
            cls.description,
            cls.key,
            cls.date_created
        ).filter_by(key=key).first()



class Title(ModelBase, Base):
    __tablename__ = "title"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255))
    id_title = Column(Integer, default=None)
    id_title_type = Column(Integer, ForeignKey("title_type.id"))
    date_created = Column(DateTime, default=datetime.utcnow())



    @classmethod
    def update(cls, session, id, description, id_title, id_title_type):
        if Title.has_id(session=session, id=id) == False:
            return False
        original = Title.find_by_id(session, id=id)
        print(description)
        print(id_title)
        print(id_title_type)
        original[0].description = description
        original.id_title = id_title
        original.id_title_type = id_title_type
        session.commit()
        session.refresh(original)
        return original


    @classmethod
    def add(cls, session, description, id_title, id_title_type):
        title = Title()
        title.description = description
        title.id_title = id_title
        title.id_title_type = id_title_type
        session.add(title)
        session.commit()
        session.refresh(title)
        return Title.find_by_id_unique(session=session, id=title.id)


    @classmethod
    def find_by_type_id(cls, session, id_title_type):
        return session.query(
            cls.id,
            cls.description,
            cls.id_title,
            cls.id_title_type,
            cls.date_created
        ).filter().all()


    @classmethod
    def find_by_id_title_belong(cls, session, id_title):
        return session.query(
            cls.id,
            cls.description,
            cls.id_title,
            cls.id_title_type,
            cls.date_created
        ).filter(Title.id_title==id_title).all()


    @classmethod
    def find_by_type_id_in(cls, session, id_title_type):
        return session.query(
            cls.id,
            cls.description,
            cls.id_title,
            cls.id_title_type,
            cls.date_created
        ).filter(Title.id_title_type.in_(id_title_type)).all()


    @classmethod
    def find_by_id(cls, session, id):
        return session.query(
            cls.id,
            cls.description,
            cls.id_title,
            cls.id_title_type,
            cls.date_created
        ).filter(Title.id==id).all()


    @classmethod
    def find_by_id_unique(cls, session, id):
        return session.query(
            cls.id,
            cls.description,
            cls.id_title,
            cls.id_title_type,
            cls.date_created
        ).filter(Title.id==id).one()


    @classmethod
    def find_by_id_father(cls, session, id_title):
        return session.query(
            cls.id,
            cls.description,
            cls.id_title,
            cls.id_title_type,
            cls.date_created
        ).filter(Title.id_title==id_title).all()


    @classmethod
    def find_by_id_father_in(cls, session, id_title):
        return session.query(
            cls.id,
            cls.description,
            cls.id_title,
            cls.id_title_type,
            cls.date_created
        ).filter(Title.id_title.in_(id_title)).all()