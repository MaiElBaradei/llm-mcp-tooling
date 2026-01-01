from pydantic import BaseModel

class FetchExchangeRateToolArgs(BaseModel):
    base_currency: str
    target_currency: str

class ExchangeRateInfo(BaseModel):
    base_currency: str
    target_currency: str
    exchange_rate: float


class ExchangeRateMetadata(BaseModel):
    provider: str
    endpoint: str
    timestamp: str


class FetchExchangeRateOutput(BaseModel):
    data: ExchangeRateInfo
    metadata: ExchangeRateMetadata
