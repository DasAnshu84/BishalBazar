from fastapi import APIRouter, HTTPException, Query
from database import supabase
from models import ClientCreate, ClientUpdate, ClientResponse
from typing import List

router = APIRouter(tags=["Clients"])

@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate):
    try:
        res = supabase.table("clients").insert(client.model_dump()).execute()
        if not res.data:
            raise HTTPException(status_code=400, detail="Failed to create client")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[ClientResponse])
def get_clients(skip: int = Query(0, ge=0), limit: int = Query(600, le=1000)):
    try:
        # Supabase range is inclusive
        res = supabase.table("clients").select("*").order("client_name", desc=False).range(skip, skip + limit - 1).execute()
        return res.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: str):
    # Ensure it's a valid UUID to prevent catching non-UUID paths
    from uuid import UUID
    try:
        UUID(client_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format")
        
    res = supabase.table("clients").select("*").eq("id", client_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Client not found")
    return res.data[0]

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: str, client: ClientUpdate):
    update_data = {k: v for k, v in client.model_dump(exclude_unset=True).items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    try:
        res = supabase.table("clients").update(update_data).eq("id", client_id).execute()
        if not res.data:
            raise HTTPException(status_code=404, detail="Client not found")
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{client_id}")
def delete_client(client_id: str):
    res = supabase.table("clients").delete().eq("id", client_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted successfully"}
