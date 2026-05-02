# Task 2: Live Market Data Fetch - Implementation Plan

This document outlines the approach to building the live market data fetcher as requested in Task 2 of the Timecell Intern Technical Test.

## User Review Required

> [!IMPORTANT]
> Please review the chosen APIs and tools. I've proposed using `yfinance` and the `CoinGecko API` (via `requests`) to show a mix of library-based and raw REST API fetching. I've also proposed using the `rich` library to create a beautiful, terminal-native table as the output.

## Open Questions

> [!NOTE]
> 1.  Are you okay with using the `rich` library for terminal formatting? It is highly regarded for terminal applications and fits the "terminal, not a dashboard" ethos of Timecell perfectly.
> 2.  Do you have a specific folder structure in mind, like creating a `timecell-intern-nisarg` folder to serve as the root of your GitHub repository? If not, I will create a `task2` folder in the current directory.

## Proposed Changes

We will create a structured Python script for this task.

### Task 2 Folder

#### [NEW] [task2_market_data.py](file:///Users/nisargbhatia/Desktop/Timecell/task2_market_data.py)
This script will contain the main logic.
*   **Dependencies**: `yfinance` (for stocks/indices), `requests` (for crypto API), `rich` (for terminal UI), and `datetime` (for timestamps).
*   **Data Fetching**:
    *   **BTC**: Fetch via CoinGecko's simple price API using standard HTTP `requests`.
    *   **NIFTY 50**: Fetch using `yfinance` (Ticker: `^NSEI`).
    *   **RELIANCE**: Fetch using `yfinance` (Ticker: `RELIANCE.NS`).
*   **Error Handling**: Wrap each fetch in a `try...except` block to ensure that if CoinGecko is down, NIFTY and RELIANCE still fetch and display successfully.
*   **Display**: Use `rich.table.Table` to create a cleanly formatted table that matches the aesthetic requested in the test.

#### [NEW] [requirements.txt](file:///Users/nisargbhatia/Desktop/Timecell/requirements.txt)
To document the dependencies:
```text
yfinance
requests
rich
```

## Verification Plan

### Automated Tests
*   Run the script multiple times to ensure data is fetched consistently.
*   Simulate an error (e.g., by querying a fake ticker) to ensure the table still renders with the other successful assets and logs the error gracefully.

### Manual Verification
*   Verify the output exactly matches the aesthetic requested (table format, currencies, timestamp).
*   Verify the prices reflect real-time market data.
