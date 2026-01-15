# JSON Schema definitions for fetch_weather tool

FETCH_WEATHER_ARGS_SCHEMA = {
    "type": "object",
    "required": ["city"],
    "properties": {
        "city": {
            "type": "string",
            "description": "The city name to fetch weather for"
        }
    }
}

WEATHER_INFO_SCHEMA = {
    "type": "object",
    "required": ["city", "temperature_celsius", "wind_speed_kmh", "condition"],
    "properties": {
        "city": {
            "type": "string"
        },
        "temperature_celsius": {
            "type": "number"
        },
        "wind_speed_kmh": {
            "type": "number"
        },
        "condition": {
            "type": "string"
        }
    }
}

WEATHER_API_METADATA_SCHEMA = {
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

FETCH_WEATHER_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["data", "metadata"],
    "properties": {
        "data": WEATHER_INFO_SCHEMA,
        "metadata": WEATHER_API_METADATA_SCHEMA
    }
}
