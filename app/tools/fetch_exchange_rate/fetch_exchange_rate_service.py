import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class ExchangeRateService:
    """
    Fetches live currency exchange rates.
    """

    ENDPOINT = "https://v6.exchangerate-api.com/v6"

    def __init__(self):
        logger.info("ExchangeRateService initialized")

    def fetch_rate(self, base: str, target: str) -> dict:
        try:
            logger.info(f"Fetching exchange rate from API: {base}/{target}")
            self.api_key = os.getenv("EXCHANGE_RATE_API_KEY")
            
            if not self.api_key:
                logger.error("EXCHANGE_RATE_API_KEY is not set")
                raise ValueError("EXCHANGE_RATE_API_KEY is not set")
            
            response = requests.get(
                self.ENDPOINT+f"/{self.api_key}/pair/{base}/{target}",
                timeout=10,
            )
            response.raise_for_status()
            logger.info("Exchange rate API request successful")

        except requests.RequestException as e:
            logger.error(f"Error fetching exchange rate from API: {e}", exc_info=True)
            if self.api_key is None:
                logger.error("EXCHANGE_RATE_API_KEY is not set")
            raise

        try:
            data = response.json()
            logger.debug(f"API response received: {data}")
            
            if "conversion_rate" not in data:
                logger.error(f"Invalid API response: missing conversion_rate. Response: {data}")
                raise ValueError("Invalid API response: missing conversion_rate")

            result = {
                "base": base,
                "target": target,
                "rate": data["conversion_rate"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "provider": "exchangerate-api.com",
                "endpoint": self.ENDPOINT
            }
            logger.info(f"Exchange rate fetched successfully: {data['conversion_rate']}")
            return result
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing exchange rate API response: {e}", exc_info=True)
            raise
