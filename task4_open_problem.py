import yfinance as yf
import argparse
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def fetch_historical_data(ticker: str):
    try:
        # We need at least 200 trading days, so we fetch 1 year
        data = yf.download(ticker, period="1y", interval="1d", progress=False)
        if data.empty:
            return None
        return data['Close']
    except Exception:
        return None

def analyze_trend(prices) -> dict:
    if hasattr(prices, "squeeze"):   #to get 1d list of prices
        prices = prices.squeeze()

    if len(prices) < 200:
        return {"error": "Not enough data for 200-day SMA."}

    # Calculate  Avg based on last 50 days and 200 days
    sma_50 = prices.rolling(window=50).mean()
    sma_200 = prices.rolling(window=200).mean()


    latest_price = float(prices.iloc[-1])

    latest_sma_50 = float(sma_50.iloc[-1])

    latest_sma_200 = float(sma_200.iloc[-1])

    # Determine Signal
    if latest_sma_50 > latest_sma_200:
        signal = "UPWARD TREND (Price is rising)"
        color = "bold green"
    elif latest_sma_50 < latest_sma_200:
        signal = "DOWNWARD TREND (Price is falling)"
        color = "bold red"
    else:
        signal = "FLAT (No clear trend)"
        color = "bold yellow"

    return {
        "current_price": latest_price,
        "sma_50": latest_sma_50,
        "sma_200": latest_sma_200,
        "signal": signal,
        "color": color
    }

def main():
    parser = argparse.ArgumentParser(description="Trend Following Indicator Tool")
    parser.add_argument("--ticker", type=str, default="RELIANCE.NS", help="Ticker symbol (e.g. RELIANCE.NS, ^NSEI, AAPL)")
    args = parser.parse_args()

    ticker = args.ticker
    console.print(f"Fetching historical data for {ticker}...\n")

    prices = fetch_historical_data(ticker)
    
    if prices is None:
        console.print(f"Failed to fetch data for {ticker}. Check the ticker symbol.")
        return
        
    analysis = analyze_trend(prices)
    
    if "error" in analysis:
        console.print(f"Analysis Error: {analysis['error']}")
        return

    # Fetch currency symbol (e.g. USD, INR) for context
    currency = yf.Ticker(ticker).info.get('currency', '')
    currency_str = f" ({currency})" if currency else ""

    # Construct the output table
    table = Table(title=f"Technical Trend Analysis: SM indicates Simple Moving Avg {ticker}", border_style="cyan")
    table.add_column("Metric", style="bold cyan")
    table.add_column(f"Value{currency_str}", style="bold white")
    
    table.add_row("Current Price", f"{analysis['current_price']:.2f}")
    table.add_row("50-Day SMA", f"{analysis['sma_50']:.2f}")
    table.add_row("200-Day SMA", f"{analysis['sma_200']:.2f}")
    
    console.print()
    console.print(table)
    
    verdict_text = f"[{analysis['color']}]{analysis['signal']}[/{analysis['color']}]"
    panel = Panel(
        f"The 50-day moving average vs the 200-day moving average suggests a trend that is:\n\n{verdict_text}",
        title="Market Signal Verdict",
        border_style="cyan",
        expand=False
    )
    console.print(panel)

if __name__ == "__main__":
    main()
