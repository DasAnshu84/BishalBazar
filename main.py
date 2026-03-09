from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Response
from typing import Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from open_router_calling import extract_ledger_from_image_bytes
from routers import clients, transactions

app = FastAPI(title="Ledger Extraction API")

app.include_router(clients.router, prefix="/api/clients")
app.include_router(transactions.router, prefix="/api/transactions")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory cache for idempotency
# In production, use Redis or database
request_cache = {}

@app.post("/extract-ledger/")
async def extract_ledger(
    file: UploadFile = File(...),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    if not idempotency_key:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")

    # Check cache
    if idempotency_key in request_cache:
        print(f"Cache hit for key: {idempotency_key}")
        cached_csv = request_cache[idempotency_key]
        return Response(content=cached_csv, media_type="application/json")
        
    print(f"Cache miss for key: {idempotency_key}. Processing image...")
    
    
    if len(request_cache) > 10:  # Simple cache eviction policy
        print("Cache limit reached. Clearing cache.")
        request_cache.clear()
    
    try:
        image_bytes = await file.read()
        csv_string = extract_ledger_from_image_bytes(image_bytes)
        
        # Save to cache
        request_cache[idempotency_key] = csv_string
        
        return Response(content=csv_string, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
