from .fetch_exchange_rate_service import ExchangeRateService
from .fetch_exchange_rate_schema import (
    ExchangeRateInfo,
    ExchangeRateMetadata,
)


class FetchExchangeRateTool:
    """
    Tool: fetch_exchange_rate
    ------------------------
    Retrieves the latest exchange rate for a currency pair.
    """

    def __init__(self):
        self.service = ExchangeRateService()

    def run(self, base_currency: str, target_currency: str) -> dict:
        result = self.service.fetch_rate(base_currency, target_currency)

        return {
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
