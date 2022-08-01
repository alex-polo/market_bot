from dataclasses import dataclass


@dataclass
class Subscription:
    market: str
    type_market: str
    signal: str
    timeframes: dict
