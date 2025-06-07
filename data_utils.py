import pandas as pd
import yfinance as yf
from joblib import Memory

memory = Memory("cache", verbose=0)

@memory.cache
def get_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download daily price data for a ticker."""
    df = yf.download(ticker, start=start, end=end, progress=False)
    return df