from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, TIMESTAMP
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from creds import db_path


DeclBase = declarative_base()


class IBMStock1(DeclBase):
    __tablename__ = "IBM_stock"
    date = Column(TIMESTAMP, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Integer


class GOOGLStock1(DeclBase):
    __tablename__ = "GOOGL_stock"
    date = Column(TIMESTAMP, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Integer


class MSFTStock1(DeclBase):
    __tablename__ = "MSFT_stock"
    date = Column(TIMESTAMP, primary_key=True)
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
