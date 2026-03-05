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
                                    "description": "Bracket label like S, V, CMP, etc"
                                },
                                "entry_type": {
                                    "type": "string",
                                    "description": "Combined, Original, or Single entry"
                                },
                                "amount": {
                                    "type": "number",
                                    "description": "Amount written in the ledger"
                                }
                            },
                            "required": ["unique_id", "entry_type", "amount"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["entries"],
                "additionalProperties": False
            }
        }
    }
