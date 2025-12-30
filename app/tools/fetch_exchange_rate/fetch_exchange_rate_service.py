import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import logging

load_dotenv()

class ExchangeRateService:
    """
    Fetches live currency exchange rates.
    """

    ENDPOINT = "https://v6.exchangerate-api.com/v6"

    def fetch_rate(self, base: str, target: str) -> dict:
        try:
            self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
            response = requests.get(
                self.ENDPOINT+f"/{self.api_key}/pair/{base}/{target}",
                timeout=10,
            )
            response.raise_for_status()

        except requests.RequestException as e:
            logging.error(f"Error fetching exchange rate: {e}")
            if self.api_key is None:
                logging.error("EXCHANGE_RATE_API_KEY is not set.")
            return {}

        data = response.json()
        print(data)

        return {
            "base": base,
            "target": target,
            "rate": data["conversion_rate"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "provider": "exchangerate-api.com",
            "endpoint": self.ENDPOINT
        }
