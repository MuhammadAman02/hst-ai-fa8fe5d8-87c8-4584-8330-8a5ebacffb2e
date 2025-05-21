from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    id: str = Field(..., description="Unique transaction ID")
    amount: float = Field(..., description="Transaction amount in Euros")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Transaction timestamp")
    sender: str = Field(..., description="Sender's account number")
    recipient: str = Field(..., description="Recipient's account number")
    description: Optional[str] = Field(None, description="Transaction description")
    ip_address: Optional[str] = Field(None, description="IP address of the transaction initiator")
    device_id: Optional[str] = Field(None, description="Device ID of the transaction initiator")