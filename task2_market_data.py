import yfinance as yf
import requests             #For Crypto Price by sending requests using APIs
from rich.console import Console
from rich.table import Table
from datetime import datetime



def get_crypt_price(asset_id: str) -> tuple[float | None, str | None]:

    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": asset_id,
        "vs_currencies": "usd"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if asset_id in data and "usd" in data[asset_id]:
            return data[asset_id]["usd"], "USD"
        else:
            Console().print(f"Asset ID '{asset_id}' not found in CoinGecko response")
            return None, None
    except requests.exceptions.RequestException as e:
        Console().print("Error getting info from CoinGecko")
        return None, None

def get_stock_price(ticker: str) -> tuple[float | None, str | None]:
    try:
        asset = yf.Ticker(ticker)
    
        # We first try and get current price from info, if it fails, we use history
        info = asset.info
        
        if "currentPrice" in info:
            price = info["currentPrice"]
        elif "regularMarketPrice" in info:
            price = info["regularMarketPrice"]
        else:
            hist = asset.history(period="1d")
            if hist.empty:
                Console.print(f"Data not there!!")
                return None, None
            price = hist['Close'].iloc[-1]
            
        currency = info.get("currency", "Unknown")
        return price, currency
    except Exception as e:
        console().print(f"Error fetching information from Yahoo")
        return None, None

def main():

    assets_to_fetch = [
        ("BTC", get_crypt_price, "bitcoin"),
        ("NIFTY", get_stock_price, "^NSEI"),
        ("RELIANCE", get_stock_price, "RELIANCE.NS"),
    ]

    results = []
    for display_name, fetch_func, identifier in assets_to_fetch:
        try:
            price, currency = fetch_func(identifier)
            if price is not None:
                results.append((display_name, price, currency))
            else:
                results.append((display_name, "ERROR"))

        except Exception as e:
            Console().print(f"Error in requests")
            results.append((display_name, "ERROR"))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")

    table = Table(show_header=True, header_style="bold magenta")

    table.add_column("Asset", style="dim", width=12)


    table.add_column("Price", justify="right")

    table.add_column("Currency", justify="center")

    for asset_name, price, currency in results:
        # Formatting price
        if isinstance(price, (int, float)):

            formatted_price = f"{price:,.2f}"
        else:
            formatted_price = str(price)
            
        table.add_row(asset_name, formatted_price, currency)

    Console().print(table)
    Console().print(f"\nData is fetched at time t = {timestamp}")

if __name__ == "__main__":
    main()
