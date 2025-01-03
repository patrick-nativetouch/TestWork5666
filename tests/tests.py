from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Transactions
from mock import patch
from app.auth import validate_api_key
import pytest
import heapq


@pytest.fixture()
def client():
    client = TestClient(app)
    client.app.dependency_overrides[validate_api_key] = lambda: True
    yield client

@pytest.fixture()
def db():
    yield SessionLocal()

@pytest.fixture()
def transaction_payload():
    return {
        "transaction_id": "test123",
        "user_id": "user1",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }

def test_create_transaction(transaction_payload, client):
    response = client.post(
        "tasks/transactions",
        json=transaction_payload
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction received"

def test_get_statistics(client, db):
    response = client.get(
        "tasks/statistics",
    )
    res = response.json()
    assert response.status_code == 200
    assert "total_transactions" in res
    assert "average_transaction_amount" in res
    assert "top_transactions" in res

    transactions = db.query(Transactions).all()
    total_transactions = len(transactions)
    average_amount = sum(t.amount for t in transactions) / total_transactions if total_transactions > 0 else 0
    top_transactions = heapq.nlargest(3, transactions, key=lambda t: t.amount)
    assert res["total_transactions"] == total_transactions
    assert res["average_transaction_amount"] == average_amount
    assert res["top_transactions"] == [{"transaction_id": t.transaction_id, "amount": t.amount} for t in top_transactions]

@patch("app.routes.delete_transactions")
def test_delete_transactions(delete_transactions, client):
    delete_transactions.return_value = {"message": "All transactions deleted", "status_code": 200}
    client.delete = delete_transactions
    response = client.delete(
        "tasks/transactions",
    )
    assert response["status_code"] == 200
    assert response["message"] == "All transactions deleted"

def test_teardown(transaction_payload, db):
    db = SessionLocal()
    db.query(Transactions).filter(Transactions.transaction_id == transaction_payload["transaction_id"]).delete()
    db.commit()
