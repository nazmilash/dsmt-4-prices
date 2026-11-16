"""Plot Unilever and Apple price performance during 2025."""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from prices import load_prices

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures" / "unilever-vs-apple-2025.png"
TICKERS = (
    ("AAPL", "Apple", "#555555"),
    ("ULVR.L", "Unilever", "#1F36C7"),
)


def main() -> None:
    fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)

    for ticker, company, color in TICKERS:
        prices = load_prices(ticker).loc[START_DATE:END_DATE]
        starting_close = prices.iloc[0]["Close"]
        performance = (prices["Close"] / starting_close - 1) * 100
        ax.plot(
            performance.index,
            performance,
            label=f"{company} ({ticker})",
            color=color,
            linewidth=1.6,
        )

    ax.axhline(0, color="#6b7280", linewidth=0.8)
    ax.set_title("Unilever vs Apple: percentage change in Close, 2 Jan - 31 Dec 2025")
    ax.set_ylabel("Change since first day (%)")
    ax.set_xlabel("Date")
    ax.set_xlim(mdates.datestr2num(START_DATE), mdates.datestr2num(END_DATE))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.grid(True, color="#d1d5db", linewidth=0.6, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend()
    ax.text(
        0.99,
        0.02,
        "Source: Yahoo Finance",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
        color="#6b7280",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=150, bbox_inches="tight")
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
