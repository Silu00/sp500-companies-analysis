import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:**************@localhost:5432/postgres")

query = """
SELECT c.ticker, c.company, c.sector,
       f.trailing_pe,
       f.profit_margin AS profit_margin_raw,
       f.market_cap
FROM comparison_by_sectors c
JOIN v_sp500_companies_fundamentals f 
    ON c.ticker = f.ticker
WHERE f.trailing_pe IS NOT NULL 
  AND f.profit_margin IS NOT NULL;
"""
df = pd.read_sql(query, engine).dropna(subset=["trailing_pe","profit_margin_raw","sector","ticker"])
df["profit_margin_pct"] = np.where(df["profit_margin_raw"].abs().median() <= 1.5,
                                   df["profit_margin_raw"]*100, df["profit_margin_raw"])

#Size of point based on market cap
if "market_cap" in df and df["market_cap"].notna().any():
    m = df["market_cap"].where(df["market_cap"] > 0)
    s = np.log10(m).replace([np.inf, -np.inf], np.nan).fillna(np.log10(m[m > 0]).median())
    s = (s - s.min()) / (s.max() - s.min() + 1e-9) * 200 + 30
else:
    s = 60
df["size"] = s

x1, x2 = df["trailing_pe"].quantile([0.01, 0.99])
y1, y2 = df["profit_margin_pct"].quantile([0.01, 0.99])
df = df[df["trailing_pe"].between(x1, x2) & df["profit_margin_pct"].between(y1, y2)].copy()

sectors = sorted(df["sector"].unique())
n = len(sectors)
cols = 3
rows = math.ceil(n / cols)

fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4), sharex=True, sharey=True)
axes = axes.ravel()

for i, sec in enumerate(sectors):
    ax = axes[i]
    d = df[df["sector"] == sec]

    med_pe, mean_pe = d["trailing_pe"].median(), d["trailing_pe"].mean()
    med_pm, mean_pm = d["profit_margin_pct"].median(), d["profit_margin_pct"].mean()
    ax.scatter(d["trailing_pe"], d["profit_margin_pct"], s=d["size"], alpha=0.7)

    ax.axvline(med_pe, ls="--", c="magenta", lw=1.2,
               label=f"Median P/E = {med_pe:.1f}")
    ax.axhline(med_pm, ls="--", c="magenta", lw=1.2,
               label=f"Median Margin = {med_pm:.1f}%")
    ax.axvline(mean_pe, ls=":", c="royalblue", lw=1.2,
               label=f"Mean P/E = {mean_pe:.1f}")
    ax.axhline(mean_pm, ls=":", c="royalblue", lw=1.2,
               label=f"Mean Margin = {mean_pm:.1f}%")

    ax.set_title(sec, fontsize=9)
    ax.grid(True, alpha=0.2)

for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

fig.suptitle("P/E vs Profit Margin by sector", y=0.995, fontsize=14)
fig.text(0.5, 0.025, "Trailing P/E", ha="center")
fig.text(0.04, 0.5, "Profit Margin (%)", va="center", rotation="vertical")

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels,
           bbox_to_anchor=(0.9, 0.5),
           loc="upper center",
           frameon=False, title="Lines meaning", fontsize=9)

plt.tight_layout(rect=[0.05, 0.05, 0.84, 0.95])
plt.show()
