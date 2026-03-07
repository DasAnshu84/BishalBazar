from fastapi import APIRouter, HTTPException, Query
from database import supabase
from models import TransactionCreate, TransactionUpdate, TransactionResponse, BulkTransactionItem
from typing import List, Optional

router = APIRouter(tags=["Transactions"])

@router.post("/", response_model=TransactionResponse)
def create_transaction(transaction: TransactionCreate):
    data = transaction.model_dump(exclude={"date"})
    data["client_id"] = str(data["client_id"]) # UUID to string for JSON serialization
    if transaction.date:
        data["created_at"] = f"{transaction.date}T00:00:00Z"
    try:
        res = supabase.table("transactions").insert(data).execute()
        if not res.data:
            raise HTTPException(status_code=400, detail="Failed to create transaction")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/bulk")
def bulk_create_transactions(items: List[BulkTransactionItem]):
    if not items:
        raise HTTPException(status_code=400, detail="No items provided")

    # Collect all unique_ids (client_codes) from the request
    unique_ids = list(set(item.unique_id for item in items if item.unique_id))
    
    # Check for empty unique_ids
    empty_ids = [i for i, item in enumerate(items) if not item.unique_id]
    if empty_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Items at indices {empty_ids} have empty unique_id. Please provide a valid client code."
        )

    # Look up all client_codes in one query
    try:
        res = supabase.table("clients").select("id, client_code").in_("client_code", unique_ids).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # Build a map: client_code -> client_id
    code_to_id = {row["client_code"]: row["id"] for row in res.data}

    # Validate all unique_ids exist
    missing_codes = [uid for uid in unique_ids if uid not in code_to_id]
    if missing_codes:
        raise HTTPException(
            status_code=400,
            detail=f"The following client codes do not exist. Please create them in the Clients table first: {missing_codes}"
        )

    # Build transaction rows
    rows = []
    for item in items:
        row = {
            "client_id": code_to_id[item.unique_id],
            "transaction_amount": item.total_amount
        }
        if item.date:
            row["created_at"] = f"{item.date}T00:00:00Z"
        rows.append(row)

    # Bulk insert
    try:
        res = supabase.table("transactions").insert(rows).execute()
        if not res.data:
            raise HTTPException(status_code=400, detail="Failed to insert transactions")
        return {
            "message": f"Successfully inserted {len(res.data)} transactions",
            "transactions": res.data
        }
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
