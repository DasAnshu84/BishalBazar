RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "ledger_entries",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "entries": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "unique_id": {
                                "type": "string",
                                "description": "The bracketed label exactly as written, e.g., (S.), (V), (CMP)"
                            },
                            "breakdown": {
                                "type": "string",
                                "description": "The formula of original numbers. For single entries, just the number (e.g., '50'). For bracketed additions, write the formula (e.g., '50 + 20')."
                            },
                            "total_amount": {
                                "type": "number",
                                "description": "The final mathematical sum of the breakdown field."
                            }
                        },
                        "required": [
                            "unique_id",
                            "breakdown",
                            "total_amount"
                        ],
                        "propertyOrdering": [
                            "unique_id",
                            "breakdown",
                            "total_amount"
                        ],
                        "additionalProperties": False
                    }
                },
                "written_page_total": {
                    "type": "number",
                    "description": "The grand total explicitly handwritten at the bottom of the ledger page."
                },
                "calculated_page_total": {
                    "type": "number",
                    "description": "The actual mathematical sum of all the original numbers to verify against the written_page_total."
                }
            },
            "required": [
                "entries",
                "written_page_total",
                "calculated_page_total"
            ],
            "propertyOrdering": [
                "entries",
                "written_page_total",
                "calculated_page_total"
            ],
            "additionalProperties": False
        }
    }
}