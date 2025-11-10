from __future__ import annotations
from pathlib import Path
import csv
from dataclasses import dataclass
from typing import List, Dict
import math
import time

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_prices.csv"

ASSETS = [
    {"symbol": "EURUSD", "name": "EUR/USD"},
    {"symbol": "SPX", "name": "S&P 500"},
    {"symbol": "XAUUSD", "name": "Gold"},
]

@dataclass
class Signal:
    symbol: str
    direction: str  # "LONG" | "SHORT" | "FLAT"
    confidence: float
    price: float
    timestamp: float

def list_assets() -> List[Dict[str, str]]:
    return ASSETS

def _load_prices() -> Dict[str, float]:
    # CSV columns: timestamp,EURUSD,SPX,XAUUSD
    last_row = None
    with open(DATA_PATH, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            last_row = row
    if not last_row:
        return {a["symbol"]: 0.0 for a in ASSETS}
    return {sym: float(last_row[sym]) for sym in ["EURUSD","SPX","XAUUSD"]}

def _toy_indicator(x: float) -> float:
    # Simple oscillator in range [-1, 1]
    return math.tanh(x)

def get_latest_signals() -> List[dict]:
    prices = _load_prices()
    t = time.time() / 3600.0
    signals: List[Signal] = []
    for idx, asset in enumerate(ASSETS):
        # generate a pseudo indicator per asset
        osc = _toy_indicator(math.sin(t + idx))
        if osc > 0.2:
            direction = "LONG"
        elif osc < -0.2:
            direction = "SHORT"
        else:
            direction = "FLAT"
        confidence = abs(osc)
        signals.append(Signal(
            symbol=asset["symbol"],
            direction=direction,
            confidence=round(confidence, 3),
            price=round(prices.get(asset["symbol"], 0.0), 4),
            timestamp=time.time()
        ))
    return [s.__dict__ for s in signals]
