from fastapi import APIRouter, HTTPException, Query
from database import supabase
from models import TransactionCreate, TransactionUpdate, TransactionResponse
from typing import List, Optional

router = APIRouter(tags=["Transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    data = transaction.model_dump()
    data["client_id"] = str(data["client_id"]) # UUID to string for JSON serialization
    try:
        res = supabase.table("transactions").insert(data).execute()
        if not res.data:
            raise HTTPException(status_code=400, detail="Failed to create transaction")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_transactions(
    date: Optional[str] = Query(None, description="Single date in YYYY-MM-DD format"),
    start_date: Optional[str] = Query(None, description="Range start date in YYYY-MM-DD format"),
    end_date: Optional[str] = Query(None, description="Range end date in YYYY-MM-DD format"),
    client_id: Optional[str] = Query(None, description="Filter by client UUID"),
    client_name: Optional[str] = None,
    client_code: Optional[str] = None,
    skip: int = Query(0, ge=0), 
    limit: int = Query(10, le=10)
):
    try:
        # We query transactions and join clients table
        query = supabase.table("transactions").select("*, clients!inner(client_name, client_code)")
        
        # Date range filter (start_date + end_date takes priority over single date)
        if start_date and end_date:
            query = query.gte("created_at", f"{start_date}T00:00:00Z").lte("created_at", f"{end_date}T23:59:59Z")
        elif start_date:
            query = query.gte("created_at", f"{start_date}T00:00:00Z")
        elif end_date:
            query = query.lte("created_at", f"{end_date}T23:59:59Z")
        elif date:
            query = query.gte("created_at", f"{date}T00:00:00Z").lte("created_at", f"{date}T23:59:59Z")

        # Client filters
        if client_id:
            query = query.eq("client_id", client_id)
        if client_name:
            query = query.eq("clients.client_name", client_name)
        if client_code:
            query = query.eq("clients.client_code", client_code)
            
        res = query.range(skip, skip + limit - 1).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{transaction_uuid}", response_model=TransactionResponse)
def get_transaction(transaction_uuid: str):
    from uuid import UUID
    try:
        UUID(transaction_uuid)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")

    res = supabase.table("transactions").select("*").eq("transaction_uuid", transaction_uuid).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return res.data[0]

@router.put("/{transaction_uuid}", response_model=TransactionResponse)
def update_transaction(transaction_uuid: str, transaction: TransactionUpdate):
    update_data = {k: v for k, v in transaction.model_dump(exclude_unset=True).items() if v is not None}
    if "client_id" in update_data:
        update_data["client_id"] = str(update_data["client_id"])
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    try:
        res = supabase.table("transactions").update(update_data).eq("transaction_uuid", transaction_uuid).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{transaction_uuid}")
def delete_transaction(transaction_uuid: str):
    res = supabase.table("transactions").delete().eq("transaction_uuid", transaction_uuid).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted successfully"}
