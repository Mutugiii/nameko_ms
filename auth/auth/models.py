import datetime

from sqlalchemy import (
    Column, Datetime
)
from sqlalchemy.ext.declarative import declarative_base


class Base(object):
    created_at = Column(
        Datetime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        Datetime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        nullable=False
    )


DeclarativeBase = declarative_base(cls=Base)