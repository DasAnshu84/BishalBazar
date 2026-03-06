# Ledger Extraction API

This API extracts data from handwritten ledger images and returns it in CSV format.
It uses OpenRouter to query the Gemini vision model.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Make sure you have a `.env` file with your OpenRouter API key:
   ```env
   OPEN_ROUTER_API_KEY=your_key_here
   ```
3. Run the API:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoint

### `POST /extract-ledger/`

Extracts ledger data from an uploaded image.

**Headers:**
- `Idempotency-Key` (required): A unique string to identify the request. If the same key is sent again, the API returns the cached CSV response instantly rather than calling the AI model again.

**Body:**
- `file` (required): The image file (e.g., `sample_image.jpeg`). Sent as `multipart/form-data`.

**Output:**
- The response is a raw CSV stream with the extracted ledger data.

## Example Request

```bash
curl -X POST "http://localhost:8000/extract-ledger/" \
     -H "Idempotency-Key: my-unique-request-123" \
     -H "accept: text/csv" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample_image.jpeg"
```


# BishalBazar APIs

This project provides APIs for extracting ledgers from images and managing `clients` and `transactions` via Supabase.

## Setup
Ensure that you have an `.env` file with `PROJECT_URL_KEY` and `SERVICE_ROLE_KEY` defined.

Start the server:
```bash
uvicorn main:app --reload
```

## API Testing with cURL

### Clients

#### Create Client
```bash
curl -X POST "http://localhost:8000/api/clients/" \
-H "Content-Type: application/json" \
-d '{"client_name": "Acme Corp", "client_code": "ACME001"}'
```

#### Get Clients (with Pagination)
```bash
# Default (skip=0, limit=10)
curl -X GET "http://localhost:8000/api/clients/" 

# Advanced Pagination
curl -X GET "http://localhost:8000/api/clients/?skip=2&limit=5"
```

#### Get Client by ID
```bash
curl -X GET "http://localhost:8000/api/clients/<CLIENT_UUID>"
```

#### Update Client
```bash
curl -X PUT "http://localhost:8000/api/clients/<CLIENT_UUID>" \
-H "Content-Type: application/json" \
-d '{"client_name": "Acme Corporation"}'
```

#### Delete Client
```bash
curl -X DELETE "http://localhost:8000/api/clients/<CLIENT_UUID>"
```

---

### Transactions

#### Create Transaction
```bash
curl -X POST "http://localhost:8000/api/transactions/" \
-H "Content-Type: application/json" \
-d '{"client_id": "<CLIENT_UUID>", "transaction_amount": 1500.50}'
```

#### Get Transactions (with Pagination and Filters)

1. **Date Range + Client ID**
```bash
curl -X GET "http://localhost:8000/api/transactions/?start_date=2024-05-01&end_date=2024-05-31&client_id=<CLIENT_UUID>"
```

2. **Date Range + Client Name**
```bash
curl -X GET "http://localhost:8000/api/transactions/?start_date=2024-05-01&end_date=2024-05-31&client_name=Acme%20Corp"
```

3. **Date Range Only**
```bash
curl -X GET "http://localhost:8000/api/transactions/?start_date=2024-05-01&end_date=2024-05-31"
```

4. **Single Date + Client Code**
```bash
curl -X GET "http://localhost:8000/api/transactions/?date=2024-05-15&client_code=ACME001"
```

5. **Just Client Name / Just Client Code**
```bash
curl -X GET "http://localhost:8000/api/transactions/?client_name=Acme%20Corp"

curl -X GET "http://localhost:8000/api/transactions/?client_code=ACME001"
```

6. **Just Pagination (limit defaults to 10)**
```bash
curl -X GET "http://localhost:8000/api/transactions/?skip=0&limit=10"
```

#### Get Transaction by ID
```bash
curl -X GET "http://localhost:8000/api/transactions/<TRANSACTION_UUID>"
```

#### Update Transaction
```bash
curl -X PUT "http://localhost:8000/api/transactions/<TRANSACTION_UUID>" \
-H "Content-Type: application/json" \
-d '{"transaction_amount": 2000.00}'
```

#### Delete Transaction
```bash
curl -X DELETE "http://localhost:8000/api/transactions/<TRANSACTION_UUID>"
```
