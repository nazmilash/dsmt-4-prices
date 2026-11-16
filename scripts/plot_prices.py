"""Plot the three stocks' adjusted-price performance since 2024."""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from prices import TICKERS, load_prices

START_DATE = "2024-01-02"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures" / "stock-prices-since-2024.png"


def main() -> None:
    fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)

    for ticker in TICKERS:
        prices = load_prices(ticker)
        starting_price = prices.loc[START_DATE, "Adj Close"]
        performance = (prices["Adj Close"] / starting_price - 1) * 100
        ax.plot(performance.index, performance, label=ticker, linewidth=1.6)

    ax.axhline(0, color="#6b7280", linewidth=0.8)
    ax.set_title("Stock performance since 2024")
    ax.set_ylabel("Change in adjusted close (%)")
    ax.set_xlabel("Date")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(True, color="#d1d5db", linewidth=0.6, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(title="Ticker")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=160, bbox_inches="tight")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
