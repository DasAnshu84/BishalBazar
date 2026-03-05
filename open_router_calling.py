import requests
import json
import base64
import os
import csv
import io
from dotenv import load_dotenv

from prompt import REFINED_LEDGER_PROMPT
from response_format import RESPONSE_FORMAT

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")
URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def encode_image_to_base64_from_bytes(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode('utf-8')

def extract_ledger_from_image_bytes(image_bytes: bytes) -> str:
    """
    Takes image bytes, calls OpenRouter API to extract ledger items,
    and returns the resulting data as a CSV string.
    """
    base64_image = encode_image_to_base64_from_bytes(image_bytes)
    data_url = f"data:image/jpeg;base64,{base64_image}"

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": REFINED_LEDGER_PROMPT
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": data_url
                    }
                }
            ]
        }
    ]

    payload = {
        "model": "google/gemini-3-flash-preview",
        "messages": messages,
        "response_format": RESPONSE_FORMAT,
        "max_tokens": 1500,
        "temperature": 0
    }

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            ledger_data = json.loads(content)
            
            entries = ledger_data.get("entries", [])
            if not entries:
                return ""
                
            output = io.StringIO()
            keys = entries[0].keys()
            dict_writer = csv.DictWriter(output, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(entries)
            return output.getvalue()
        else:
            raise ValueError(f"Unexpected response format: {data}")
            
    except Exception as e:
        print(f"Error extracting ledger: {e}")
        raise e

if __name__ == "__main__":
    image_path = "sample_image.jpeg"
    with open(image_path, "rb") as f:
        csv_string = extract_ledger_from_image_bytes(f.read())
        print(csv_string)
        with open("output.csv", "w", encoding="utf-8") as out_file:
            out_file.write(csv_string)
        print(f"Saved directly invoked run to output.csv")
