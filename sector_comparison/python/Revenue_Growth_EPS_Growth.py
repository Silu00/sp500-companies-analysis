import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:**********@localhost:5432/postgres")

query = """
SELECT 
    c.ticker, 
    c.company, 
    c.sector,
    f.revenue_growth,
    f.eps_growth,
    f.market_cap
FROM comparison_by_sectors c
JOIN v_sp500_companies_fundamentals f 
    ON c.ticker = f.ticker
WHERE f.revenue_growth IS NOT NULL 
  AND f.eps_growth IS NOT NULL;
"""

df = pd.read_sql(query, engine).dropna(subset=["revenue_growth","eps_growth","sector","ticker"]).copy()

for col in ["revenue_growth", "eps_growth"]:
    if df[col].abs().median() <= 1.5:
        df[col] = df[col] * 100.0

if "market_cap" in df.columns and df["market_cap"].notna().any():
    m = df["market_cap"].where(df["market_cap"] > 0)
    s = np.log10(m).replace([np.inf, -np.inf], np.nan).fillna(np.log10(m[m>0]).median())
    s = (s - s.min()) / (s.max() - s.min() + 1e-9) * 200 + 30
else:
    s = 60
df["size"] = s

#Trim extremes (1–99 percentile) for better plot clarity
x1, x2 = df["revenue_growth"].quantile([0.01, 0.99])
y1, y2 = df["eps_growth"].quantile([0.01, 0.99])
df_plot = df[df["revenue_growth"].between(x1, x2) & df["eps_growth"].between(y1, y2)].copy()

#TOP 5 by combined score definition: sum of growth values
df_pos = df_plot[(df_plot["revenue_growth"] > 0) & (df_plot["eps_growth"] > 0)].copy()
df_pos["score"] = df_pos["revenue_growth"] + df_pos["eps_growth"]
top5 = df_pos.nlargest(5, "score")

figdir = Path("figures"); figdir.mkdir(exist_ok=True)
fig, ax = plt.subplots(figsize=(10, 6))

for sec, g in df_plot.groupby("sector"):
    ax.scatter(g["revenue_growth"], g["eps_growth"],
               s=g["size"], alpha=0.7, label=sec)

ax.axvline(df_plot["revenue_growth"].median(), ls="--", c="magenta", lw=1,
           label=f"Median Revenue = {df_plot['revenue_growth'].median():.1f}%")
ax.axhline(df_plot["eps_growth"].median(), ls="--", c="royalblue", lw=1,
           label=f"Median EPS = {df_plot['eps_growth'].median():.1f}%")

ax.scatter(top5["revenue_growth"], top5["eps_growth"],
           s=top5["size"], facecolors='none', edgecolors='gold', linewidths=2.0,
           zorder=3, label="Top 5 (sum of %)")
for _, r in top5.iterrows():
    ax.annotate(r["ticker"],
                (r["revenue_growth"], r["eps_growth"]),
                textcoords="offset points", xytext=(6, 6), fontsize=9, weight="bold")

ax.set_xlabel("Revenue Growth (%)")
ax.set_ylabel("EPS Growth (%)")
ax.set_title("Revenue Growth vs EPS Growth- by sectors with TOP 5")
ax.grid(True, alpha=0.25)
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)

fig.tight_layout()
plt.show()
