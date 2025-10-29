import yfinance as yf
import pandas as pd

# --- Get Simulated Budget Data ---
def get_budget_data():
    data = {
        "Sector": [
            "Infrastructure", "Energy", "Agriculture",
            "FMCG", "IT", "Healthcare", "Auto"
        ],
        "Budget_2023": [2.4, 1.1, 1.6, 0.8, 0.6, 1.2, 0.9],
        "Budget_2024": [2.7, 1.3, 1.9, 0.9, 0.7, 1.4, 1.1],
    }

    df = pd.DataFrame(data)
    df["Change_%"] = ((df["Budget_2024"] - df["Budget_2023"]) / df["Budget_2023"]) * 100
    return df


# --- Get Stock Performance Data (Clean Version) ---
def get_sector_performance(tickers):
    results = []

    for sector, ticker in tickers.items():
        stock = yf.download(ticker, start="2024-01-01", end="2024-06-30", progress=False)

        if stock.empty:
            results.append({
                "Sector": sector,
                "Ticker": ticker,
                "Stock_Performance_%": None
            })
            continue

        # Calculate % change between first and last closing price
        start_price = stock["Close"].iloc[0]
        end_price = stock["Close"].iloc[-1]
        performance = ((end_price - start_price) / start_price) * 100

        # Append clean numeric values
        results.append({
            "Sector": sector,
            "Ticker": ticker,
            "Stock_Performance_%": round(float(performance), 2)
        })

    return pd.DataFrame(results)
