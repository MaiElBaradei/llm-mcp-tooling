# JSON Schema definitions for fetch_exchange_rate tool

FETCH_EXCHANGE_RATE_ARGS_SCHEMA = {
    "type": "object",
    "required": ["base_currency", "target_currency"],
    "properties": {
        "base_currency": {
            "type": "string",
            "description": "The base currency code (e.g., USD, EUR)"
        },
        "target_currency": {
            "type": "string",
            "description": "The target currency code (e.g., USD, EUR)"
        }
    }
}

EXCHANGE_RATE_INFO_SCHEMA = {
    "type": "object",
    "required": ["base_currency", "target_currency", "exchange_rate"],
    "properties": {
        "base_currency": {
            "type": "string"
        },
        "target_currency": {
            "type": "string"
        },
        "exchange_rate": {
            "type": "number"
        }
    }
}

EXCHANGE_RATE_METADATA_SCHEMA = {
    "type": "object",
    "required": ["provider", "endpoint", "timestamp"],
    "properties": {
        "provider": {
            "type": "string"
        },
        "endpoint": {
            "type": "string"
        },
        "timestamp": {
            "type": "string"
        }
    }
}

FETCH_EXCHANGE_RATE_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["data", "metadata"],
    "properties": {
        "data": EXCHANGE_RATE_INFO_SCHEMA,
        "metadata": EXCHANGE_RATE_METADATA_SCHEMA
    }
}
