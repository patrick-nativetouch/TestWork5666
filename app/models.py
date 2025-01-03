from sqlalchemy import create_engine, Column, String, Float, DateTime
from .database import Base
from datetime import datetime


class Transactions(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True, unique=True, index=True)
    user_id = Column(String)
    amount = Column(Float)
    currency = Column(String)
    timestamp = Column(DateTime, default=datetime.now())
