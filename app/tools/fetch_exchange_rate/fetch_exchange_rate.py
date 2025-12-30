from .fetch_exchange_rate_service import ExchangeRateService
from .fetch_exchange_rate_schema import (
    ExchangeRateInfo,
    ExchangeRateMetadata,
)
import logging

logger = logging.getLogger(__name__)


class FetchExchangeRateTool:
    name = "fetch_exchange_rate"
    description = (
        "Retrieves the latest exchange rate for a currency pair. "
        "Returns the exchange rate along with provider and timestamp metadata."
    )

    def __init__(self):
        self.service = ExchangeRateService()
        logger.info("FetchExchangeRateTool initialized")

    def run(self, base_currency: str, target_currency: str) -> dict:
        try:
            logger.info(f"Fetching exchange rate: {base_currency} to {target_currency}")
            result = self.service.fetch_rate(base_currency, target_currency)
            
            if not result:
                logger.error("Failed to fetch exchange rate: empty result")
                raise ValueError("Failed to fetch exchange rate")

            response = {
                "data": {
                    "base_currency": base_currency,
                    "target_currency": target_currency,
                    "exchange_rate": result["rate"],
                },
                "metadata": {
                    "provider": result["provider"],
                    "endpoint": result["endpoint"],
                    "timestamp": result["timestamp"],
                },
            }
            logger.info(f"Exchange rate fetched successfully: {result['rate']}")
            return response
        except Exception as e:
            logger.error(f"Error fetching exchange rate: {e}", exc_info=True)
            raise
