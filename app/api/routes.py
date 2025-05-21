from fastapi import APIRouter, Depends
from app.models.transaction import Transaction
from app.services.fraud_detection import FraudDetectionService

router = APIRouter()

@router.get('/ping')
async def ping_pong():
    """A simple ping endpoint."""
    return {"message": "pong!"}

@router.post('/detect-fraud')
async def detect_fraud(transaction: Transaction, fraud_service: FraudDetectionService = Depends()):
    """Detect potential fraud in a transaction."""
    fraud_result = fraud_service.detect_fraud(transaction)
    return {
        "transaction_id": transaction.id,
        "fraud_detection_result": fraud_result
    }