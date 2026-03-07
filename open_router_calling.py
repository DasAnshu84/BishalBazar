from collections import defaultdict
import re

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
            
            # Process the AI response and convert to json string
            return process_ai_response(entries)
    
        else:
            raise ValueError(f"Unexpected response format: {data}")
            
    except Exception as e:
        print(f"Error extracting ledger: {e}")
        raise e
    
def process_ai_response(entries):
    # Process the AI response data as needed
    
    #Set up our deterministic grouped dictionary
    grouped_data = defaultdict(lambda: {"breakdown_list": [], "grand_total": 0})
    
    # Process line-by-line
    for entry in entries:
        # NORMALIZATION: Regex to remove brackets, parentheses, and periods
        # "(S.)" -> "S", "(C.M.P.)" -> "CMP"
        clean_id = re.sub(r'[^a-zA-Z0-9]', '', entry["unique_id"]).upper()
        
        # AGGREGATION & MATH
        grouped_data[clean_id]["breakdown_list"].append(entry["breakdown"])
        grouped_data[clean_id]["grand_total"] += entry["total_amount"]

    # 4. Format the final output
    final_results = []
    for unique_id, data in grouped_data.items():
        final_results.append({
            "unique_id": unique_id,
            "combined_breakdown": " + ".join(data["breakdown_list"]),
            "total_amount": data["grand_total"]
        })
    return json.dumps(final_results, indent=2)

if __name__ == "__main__":
    image_path = "sample_image.jpeg"
    with open(image_path, "rb") as f:
        csv_string = extract_ledger_from_image_bytes(f.read())
        print(csv_string)
        with open("output.csv", "w", encoding="utf-8") as out_file:
            out_file.write(csv_string)
        print(f"Saved directly invoked run to output.csv")
