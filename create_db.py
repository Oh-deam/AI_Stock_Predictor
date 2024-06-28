from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import datetime, json, random
from creds import db_path


DeclBase = declarative_base()


class IBMStock1(DeclBase):
    __tablename__ = "IBM_stock"
    datetime = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Integer


class GOOGLStock1(DeclBase):
    __tablename__ = "GOOGL_stock"
    datetime = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Integer


class TSCDYStock1(DeclBase):
    __tablename__ = "TSCDY_stock"
    datetime = Column(Date, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Integer


if __name__ == "__main__":
    engine = create_engine(db_path)
    SessionClass = sessionmaker(bind=engine)
    db_session = SessionClass()
    DeclBase.metadata.create_all(engine)
    db_session.commit()
