import re

FINANCE_KEYWORDS = {
    "stock", "stocks", "market", "markets", "earnings", "revenue", "ipo",
    "dividend", "dividends", "earnings", "fed", "inflation", "cpi", "sec",
    "ticker", "shares", "buy", "sell", "price", "valuation", "p/e", "pe",
    "earnings", "guidance", "analyst", "merger", "acquisition", "earnings", "eps",
}

TICKER_REGEX = re.compile(r"^[A-Z]{1,5}(\.[A-Z]{1,3})?$")


def is_valid_ticker(symbol: str) -> bool:
    """Basic ticker validation: 1-5 uppercase letters, optional dot suffix (eg BRK.A)."""
    if not symbol or not isinstance(symbol, str):
        return False
    symbol = symbol.strip().upper()
    return bool(TICKER_REGEX.match(symbol))


def is_finance_query(text: str) -> bool:
    """Heuristic check whether a free-text query is finance-related.

    Returns True if at least one finance keyword or a ticker-like token appears.
    """
    if not text or not isinstance(text, str):
        return False
    txt = text.lower()
    # check keywords
    for kw in FINANCE_KEYWORDS:
        if kw in txt:
            return True
    # check tokens for ticker-like patterns
    tokens = re.findall(r"\b[A-Za-z\.]{1,6}\b", text)
    for t in tokens:
        if TICKER_REGEX.match(t.upper()):
            return True
    return False
