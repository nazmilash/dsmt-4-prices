"""A small MCP server that fetches daily prices from Yahoo Finance."""

import yfinance as yf
from mcp.server import MCPServer

mcp = MCPServer("market-data")


@mcp.tool()
def get_prices(ticker: str, start: str, end: str) -> str:
    """Return daily prices for a ticker between two ISO dates, as CSV.

    The end date is excluded. Prices are in the currency the stock trades in:
    pence for London tickers such as ULVR.L.
    """
    df = yf.download(ticker, start=start, end=end, auto_adjust=False,
                     multi_level_index=False, progress=False)
    if df.empty:
        return f"No data for {ticker} between {start} and {end}."
    return df.round(4).to_csv()


if __name__ == "__main__":
    mcp.run()