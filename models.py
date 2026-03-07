from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

# --- CLIENT MODELS ---

class ClientBase(BaseModel):
    client_name: str
    client_code: str

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    client_name: Optional[str] = None
    client_code: Optional[str] = None

class ClientResponse(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# --- TRANSACTION MODELS ---

class TransactionBase(BaseModel):
    client_id: UUID
    transaction_amount: float

class TransactionCreate(TransactionBase):
    date: Optional[str] = None  # Optional date in YYYY-MM-DD format, defaults to now

class BulkTransactionItem(BaseModel):
    unique_id: str  # Maps to client_code in clients table
    combined_breakdown: str
    total_amount: float
    date: Optional[str] = None  # Optional date in YYYY-MM-DD format

class TransactionUpdate(BaseModel):
    client_id: Optional[UUID] = None
    transaction_amount: Optional[float] = None

class TransactionResponse(TransactionBase):
    transaction_uuid: UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None
    updated_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
