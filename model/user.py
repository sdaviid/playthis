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


class User(ModelBase, Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user = Column(String(255))
    password = Column(String(255))
    date_created = Column(DateTime, default=datetime.utcnow())


    @classmethod
    def make_login(cls, session, user, password):
        return session.query(
            cls.id,
            cls.user,
            cls.password,
            cls.date_created
        ).filter(User.user == user, User.password == password).all()