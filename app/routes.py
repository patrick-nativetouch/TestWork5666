from fastapi import APIRouter, Depends, HTTPException
from .schemas import TransactionCreate, StatisticsResponse
from .models import Transactions
from .database import SessionLocal
from .service import celery_app, redis_client
from .auth import validate_api_key
from .tasks import update_statistics
import json


router = APIRouter(dependencies=[Depends(validate_api_key)])


# POST /transactions
@router.post("/transactions")
def create_transaction(transaction: TransactionCreate):
    db = SessionLocal()

    existing_transaction = db.query(Transactions).filter(
        Transactions.transaction_id == transaction.transaction_id
    ).first()
    if existing_transaction:
        raise HTTPException(status_code=400, detail="Transaction ID must be unique")
    db_transaction = Transactions(**transaction.model_dump())
    try:
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
    except Exception as err:
        db.rollback()
        raise HTTPException(status_code=400, detail=err)
    finally:
        db.close()
    
    task = celery_app.send_task('app.tasks.update_statistics')
    return {"message": "Transaction received", "task_id" : task.task_id}

# DELETE /transactions
@router.delete("/transactions")
def delete_transactions():
    db = SessionLocal()
    db.query(Transactions).delete()
    db.commit()
    
    redis_client.flushdb()
    return {"message": "All transactions deleted"}

# GET /statistics
@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics():
    cached_stats = redis_client.get("statistics")
    if not cached_stats:
        update_statistics()
        cached_stats = redis_client.get("statistics")
    return json.loads(cached_stats)
