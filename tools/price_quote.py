#!/usr/bin/env python3
"""Price quote tool using SFI Reference Asset Oracle on Base."""

DESCRIPTION = "Fetch token/USD price via SFI Reference Asset Oracle on Base. Supports BTC, ETH, WBTC, WETH, or arbitrary 0x addresses."

import subprocess
import json
from pathlib import Path

def run(token="BTC"):
    """
    token: str - token symbol (BTC, ETH, WBTC, WETH) or 0x address
    returns: str - JSON with token, address, usd_price, raw_price, oldest_timestamp, chain, registered_oracle
    """
    result = subprocess.run(
        ["node", str(Path.home() / "Iter" / "tools" / "price_quote.js"), token],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        return f"Error: {result.stderr.strip()[:400]}"
    return result.stdout.strip()
