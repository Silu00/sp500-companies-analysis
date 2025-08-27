import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:***********@localhost:5432/postgres")

query_sql = """
SELECT 
    c.sector,
    SUM(f.market_cap) AS total_market_cap
FROM comparison_by_sectors c
JOIN v_sp500_companies_fundamentals f 
    ON c.ticker = f.ticker
WHERE f.market_cap IS NOT NULL
GROUP BY c.sector
ORDER BY total_market_cap DESC;
"""
df = pd.read_sql(query_sql, engine)
df = df.sort_values("total_market_cap", ascending=False).reset_index(drop=True)

sectors = df["sector"].tolist()
values = df["total_market_cap"].values
total = values.sum()

colors = plt.cm.tab20.colors if len(sectors) > 10 else plt.cm.Set3.colors

explode = [0.06] + [0]*(len(values)-1)

def autopct_fmt(pct):
    return f"{pct:.1f}%" if pct >= 1.0 else ""

fig, ax = plt.subplots(figsize=(9, 9))
wedges, texts, autotexts = ax.pie(
    values,
    labels=None,
    autopct=autopct_fmt,
    pctdistance=0.78,
    startangle=90,
    counterclock=False,
    explode=explode,
    colors=colors[:len(values)],
    wedgeprops={"edgecolor":"white", "linewidth":1},
    textprops={"fontsize":10}
)
centre_circle = plt.Circle((0, 0), 0.55, fc="white")
ax.add_artist(centre_circle)

def human_readable(x):
    for unit in ["", "K", "M", "B", "T"]:
        if abs(x) < 1000:
            return f"{x:.0f}{unit}"
        x /= 1000.0
    return f"{x:.0f}T"

ax.text(0, 0.02, "Total", ha="center", va="center", fontsize=10)
ax.text(0, -0.07, human_readable(total), ha="center", va="center", fontsize=14, weight="bold")

percent = values / total * 100
legend_labels = [f"{s} — {p:>4.1f}%  ({human_readable(v)})" for s, p, v in zip(sectors, percent, values)]
leg = ax.legend(
    wedges, legend_labels,
    title="Sector in (%)",
    loc="center left",
    bbox_to_anchor=(1.02, 0.5),
    frameon=False,
    fontsize=10,
    title_fontsize=11
)
ax.set_title("Market cap by sectors (S&P 500)", fontsize=13, pad=14)
ax.set_aspect("equal")
plt.show()
