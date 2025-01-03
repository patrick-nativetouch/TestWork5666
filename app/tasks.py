from .service import celery_app, redis_client
from .models import Transactions
from .database import SessionLocal
import heapq
import json


@celery_app.task
def update_statistics():
    db = SessionLocal()
    transactions = db.query(Transactions).all()
    total_transactions = len(transactions)
    average_amount = sum(t.amount for t in transactions) / total_transactions if total_transactions > 0 else 0
    top_transactions = heapq.nlargest(3, transactions, key=lambda t: t.amount)

    statistics = {
        "total_transactions": total_transactions,
        "average_transaction_amount": average_amount,
        "top_transactions": [
            {"transaction_id": t.transaction_id, "amount": t.amount} for t in top_transactions
        ]
    }
    redis_client.set("statistics", json.dumps(statistics))
    print("Statistics updated and cached")
