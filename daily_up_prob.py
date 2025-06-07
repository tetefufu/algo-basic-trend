import pandas as pd
import yfinance as yf


def get_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download daily price data for a ticker."""
    df = yf.download(ticker, start=start, end=end, progress=False)
    return df


def compute_up_indicator(df: pd.DataFrame) -> pd.Series:
    """Return a Series of 1 if close is higher than previous day's close, else 0."""
    up = df['Close'].diff().gt(0).astype(int)
    return up


def compute_statistics(up: pd.Series, max_days: int = 4):
    """Return lag correlations and conditional probabilities for up indicator."""
    lag_corr = {}
    cond_prob = {}
    for n in range(1, max_days + 1):
        lag_corr[n] = up.corr(up.shift(n))
        cond = up.shift(1).rolling(n).mean() == 1
        cond_prob[n] = up[cond].mean()
    return lag_corr, cond_prob


def analyze_tickers(tickers, start="2024-01-01", end="2025-01-01"):
    for ticker in tickers:
        print(f"--- {ticker} ---")
        df = get_stock_data(ticker, start=start, end=end)
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
    analyze_tickers(["AAPL", "MSFT", "GOOG"])
