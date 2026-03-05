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
