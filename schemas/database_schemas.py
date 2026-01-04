from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class T_funds(Base):

    __tablename__ = "t_funds"

    fnd_id = Column(Integer, primary_key=True, index=True)
    fnd_account = Column(String)
    fnd_type = Column(String)
    fnd_amount = Column(Float)
    fnd_active_flag = Column(String)

class T_transactions(Base):

    __tablename__ = "t_transactions"

    txn_id = Column(Integer, primary_key=True, index=True)
    txn_account = Column(String)
    txn_date = Column(Date)
    txn_amount = Column(Float)
    txn_type = Column(String)
    txn_tag = Column(String)
    txn_active_flag = Column(String)