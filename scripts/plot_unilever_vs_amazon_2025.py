"""Plot Unilever and Amazon price performance during 2025."""

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import yfinance as yf

START_DATE = "2025-01-01"
END_DATE = "2026-01-01"
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "figures" / "unilever-vs-amazon-2025.png"
TICKERS = (
    ("ULVR.L", "Unilever", "#1F36C7"),
    ("AMZN", "Amazon", "#555555"),
)


def main() -> None:
    fig, ax = plt.subplots(figsize=(11, 6), constrained_layout=True)

    for ticker, company, color in TICKERS:
        prices = yf.download(
            ticker,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=False,
            multi_level_index=False,
            progress=False,
        )
        if prices.empty:
            raise RuntimeError(
                f"No Yahoo Finance data for {ticker} "
                f"between {START_DATE} and {END_DATE}."
            )
        performance = (prices["Close"] / prices.iloc[0]["Close"] - 1) * 100
        ax.plot(
            performance.index,
            performance,
            label=f"{company} ({ticker})",
            color=color,
            linewidth=1.6,
        )

    ax.axhline(0, color="#6b7280", linewidth=0.8)
    ax.set_title("Unilever vs Amazon: percentage change in Close, 2 Jan - 31 Dec 2025")
    ax.set_ylabel("Change since first day (%)")
    ax.set_xlabel("Date")
    ax.set_xlim(mdates.datestr2num(START_DATE), mdates.datestr2num("2025-12-31"))
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
    plt.close(fig)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
