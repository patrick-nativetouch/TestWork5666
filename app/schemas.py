from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class TransactionCreate(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    currency: str = Field(..., min_length=1)
    timestamp: datetime

class StatisticsResponse(BaseModel):
    total_transactions: int
    average_transaction_amount: float
    top_transactions: List[dict]