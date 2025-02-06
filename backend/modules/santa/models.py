from datetime import datetime
from typing import List

from database import engine
from pydantic import BaseModel
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Table,
                        func)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

blacklist = Table(
    'blacklist',
    Base.metadata,
    Column('participant_id', Integer, ForeignKey('participants.id')),
    Column('blacklisted_id', Integer, ForeignKey('participants.id'))
)


class Participant(Base):
    __tablename__ = 'participants'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    blacklisted = relationship(
        'Participant',
        secondary=blacklist,
        primaryjoin=id == blacklist.c.participant_id,
        secondaryjoin=id == blacklist.c.blacklisted_id
    )


class Draw(Base):
    __tablename__ = 'draws'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=func.now())
    assignments = relationship('Assignment')


class Assignment(Base):
    __tablename__ = 'assignments'

    id = Column(Integer, primary_key=True)
    draw_id = Column(Integer, ForeignKey('draws.id'))
    giver_id = Column(Integer, ForeignKey('participants.id'))
    receiver_id = Column(Integer, ForeignKey('participants.id'))

    giver = relationship('Participant', foreign_keys=[giver_id])
    receiver = relationship('Participant', foreign_keys=[receiver_id])




Base.metadata.create_all(bind=engine)



