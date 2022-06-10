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



class DataSource(ModelBase, Base):
    __tablename__ = 'data_source'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255))
    key = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def find_by_key(cls, session, key):
        return session.query(
            cls.id,
            cls.description,
            cls.key,
            cls.date_created
        ).filter_by(key=key).first()