import pandas as pd
from data_utils import get_stock_data


def compute_up_indicator(df: pd.DataFrame) -> pd.Series:
    """Return a Series of 1 if close is higher than previous day's close, else 0."""
    # Handle MultiIndex columns (e.g., from yfinance)
    if isinstance(df.columns, pd.MultiIndex):
        close = df['Close']
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]  # Take the first column if multiple
    else:
        close = df['Close']
    close = close.squeeze()  # Ensure it's a Series
    up = close.diff().gt(0).astype(int)
    return up


def compute_statistics(up: pd.Series, max_days: int = 4):
    """Return lag correlations and conditional probabilities for up indicator."""
    lag_corr = {}
    cond_prob = {}
    for n in range(1, max_days + 1):
        lag_corr[n] = up.corr(up.shift(n))
        cond = (up.shift(1).rolling(n).mean() == 1).fillna(False)
        cond_prob[n] = up[cond].mean()
    return lag_corr, cond_prob


def analyze_tickers(tickers, start="2024-01-01", end="2025-01-01"):
    for ticker in tickers:
        print(f"--- {ticker} ---")
        df = get_stock_data(ticker, start=start, end=end)
        if df.empty:
            print("No data for this ticker.")
            continue
        up = compute_up_indicator(df)
        lag_corr, cond_prob = compute_statistics(up)
        print("Lag correlations (corr with previous n days):")
        for n, c in lag_corr.items():
            print(f"  Lag {n}: {c:.3f}")
        print("Probability next day is up if previous n days were all up:")
        for n, p in cond_prob.items():
            print(f"  {n} days up -> {p:.3f}")
        print()


if __name__ == "__main__":
    tickers = [
        # High volume stocks
        "AAPL", "MSFT", "GOOG",
        # Low volume stocks (examples, may change over time)
        "GNLN", "TIRX", "RHE",
        # High volume crypto (Yahoo Finance tickers)
        "BTC-USD", "ETH-USD",
        # Low volume crypto (examples)
        "DOGE-USD", "ZRX-USD",
        # Commodities
        "GC=F",   # Gold Futures
        "CL=F",   # Crude Oil Futures
        "SI=F",   # Silver Futures
        # Index funds / ETFs
        "SPY",    # S&P 500 ETF
        "QQQ",    # Nasdaq 100 ETF
        "VTI",    # Total Stock Market ETF
        "EFA",    # MSCI EAFE ETF
    ]
    analyze_tickers(tickers)
