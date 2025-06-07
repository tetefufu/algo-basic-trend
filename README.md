# algo-basic-trend

This repository contains a simple example for analysing whether a stock's daily
close ends up or down from the previous day using 2024 market data. The
`daily_up_prob.py` script downloads prices with **yfinance** and calculates:

- Correlation between the up/down indicator and its values over the previous
  1--4 days.
- The probability that a day closes higher, provided the previous `n` days were
  all higher (`n` from 1 to 4).

## Usage

Run the script with Python. It uses yfinance to fetch data, so an internet
connection and the `yfinance` package are required:

```bash
pip install yfinance
python3 daily_up_prob.py
```

By default it analyses AAPL, MSFT and GOOG for the 2024 calendar year. You can
edit the ticker list in the `main` block or call `analyze_tickers` with your
own list of symbols.
