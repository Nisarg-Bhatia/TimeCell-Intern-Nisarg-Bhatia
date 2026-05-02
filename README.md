# Timecell Project Implementation


## Task 01 - Portfolio Risk Calculator

This task implements a terminal-based portfolio risk calculator. It evaluates a portfolio's resilience against market crashes by simulating different severity scenarios.

### Features

- **Simulation Engine**: Simulates the impact of market crashes (e.g., 100% full crash, 50% moderate crash) on the total portfolio value.

- **Runway Calculation**: Calculates a "Survival Runway" (in months) based on the post-crash portfolio value and monthly expenses. The portfolio must maintain >12 months of runway to "PASS" the ruin test.

- **Concentration Risk Warning**: Actively monitors and warns if any single asset exceeds a 40% allocation threshold.

- **Risk Driver Identification**: Calculates risk scores to identify the specific asset contributing the most to potential portfolio losses.



## Task 02 — Live Market Data Fetch

This task is to build an application to fetch real-time market data across both traditional finance and cryptocurrency markets. 

The application fetches the current price of assets such as Bitcoin, Nifty 50, Reliance Industries, etc and displays them in table.

---

### Libraries Used

#### 1. `yfinance`
* It Yahoo's publicly available APIs to fetch market data.
* It doesn't require creating any API keys.
* Used inside the `fetch_stock_price(ticker)` function to retrieve real-time prices for NIFTY 50 (`^NSEI`) and Reliance Industries (`RELIANCE.NS`).

#### 2. `requests`
* Its a Python library for making REST API calls.
* Used to call the CoinGecko API directly.
* Used inside the `fetch_crypto_price(asset_id)` function to send a GET request to CoinGecko's `/simple/price` endpoint and parse the resulting JSON.


#### 3. `datetime`
* Its a Python's standard library module for manipulating dates and times.

---


### Error Handling

Errors are handled as follows:
- If an API rate-limits the request, times out, or returns a 404, the `try...except` block in the specific fetcher function catches it.
- An error message is displayed and function returns `(None, None)`.

---

## Task 03 — AI-Powered Portfolio Explainer


This section gives insight of the implementation of **Task 3: AI-Powered Portfolio Explainer**. The `task3_portfolio_explainer.py` script uses Google's Gemini LLM to analyze a financial portfolio and explain its risks to a non-expert client who doesn't know much about advanced financial terms.


# LLM Chosen for this task is 'Gemini-2.5-flash'

- I attempted to run the same code against the Anthropic Claude API for comparison but encountered a credit balance issue on the free tier.
- I chose gemini because it gave accurate, well-structured output and correctly identified several risk factors 
- The model also correctly referenced specific numbers 
- Gemini also supports native Pydantic schema via `response_schema`

### Features Implemented are as follows:

- **Portfolios as Input**: The script accepts an external portfolio via a JSON file using the `--portfolio` argument. 
- **Raw and Structured Outputs**: The script prints the raw JSON response received from the API before rendering. Then it gives structured output too.



### Prompt Engineering Approach

I used an iterative approach for prompt building. 
Initially, I tried a basic prompt: *"Explain this portfolio to me"*. However, standard text generation is difficult to parse due to inconsistent formatting.

I changed the approach from generating free-form text to generating **Structured JSON Data**. 
1. **Pydantic Models**: I defined a rigid `PortfolioExplanation` schema in Python using Pydantic.
2. **Schema** : I passed this schema directly to Gemini so that LLM follows the requested keys (`summary`, `doing_well`, `consider_changing`, `verdict`). 

**The Prompt I used:**
The actual prompt from the code is:

```python
prompt = f"""
You are a {tone} financial advisor talking to a non-expert client. 
Review the following portfolio and provide a risk assessment. 
Speak directly to the client (e.g. "You have a...").

Portfolio Details are as shown:
{json.dumps(portfolio, indent=2)}
"""
```


## Task 04 — The Open Problem (Trend Following Indicator)

This task implements a CLI tool for wealth management that calculates the market trend of any given asset. It fetches 1 year of historical daily price data and uses Simple Moving Averages (SMA) to determine if an asset is currently in an upward or downward trend.

### Features
- **Dynamic Asset Selection**: Pass any valid Yahoo Finance ticker (e.g., `AAPL`, `RELIANCE.NS`, `BTC-USD`, `^NSEI`) via the `--ticker` CLI argument.

- **Trend Calculation**: Calculates the 50-day and 200-day Simple Moving Averages (SMA) to determine momentum.

  - **Upward Trend**: The 50-day SMA crosses above the 200-day SMA.

  - **Downward Trend**: The 50-day SMA crosses below the 200-day SMA.

- **Dynamic Currency Context**: Automatically queries the asset's underlying currency (e.g., USD, INR) and displays it directly in the data table for accurate context.

### Challenges

**What was the hardest part, and how did I approach it?**
- The most challenging aspect of this task was handling the unpredictable data structures returned by the `yfinance` library.By dynamically checking for and utilizing the pandas `.squeeze()` method, the script forces any complex, single-column DataFrames to flatten into a predictable 1D Series. This approach ensures that the moving average engine remains robust and crash-free regardless of how the API formats the incoming payload. 
- Also, handling APIs and choosing a suitable free tier LLM for Task 3 was a challenge.
