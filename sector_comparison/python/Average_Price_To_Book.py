import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:*************@localhost:5432/postgres")

query = """
    SELECT s.sector, AVG(f.price_to_book) AS avg_price_to_book
    FROM v_sp500_companies_fundamentals f
    JOIN comparison_by_sectors s
        ON f.ticker = s.ticker
    WHERE trailing_pe IS NOT NULL
    GROUP BY s.sector
    ORDER BY avg_price_to_book DESC 
"""
df = pd.read_sql(query, engine)

plt.rcParams['figure.facecolor'] = '#333333'
plt.rcParams['axes.facecolor'] = '#3c3c3c'
plt.figure(figsize=(14, 7))

barplot = sns.barplot(
    x='sector',
    y='avg_price_to_book',
    data=df,
    hue='sector',
    palette='Spectral',
    edgecolor='white',
    linewidth=0.8,
    alpha=0.95
)

plt.title('Price to book by sectors', fontsize=18, weight='bold', color='white', pad=20)
plt.xlabel('Sector', fontsize=14, weight='bold', color='white')
plt.ylabel('Price to book', fontsize=14, weight='bold', color='white')

plt.xticks(rotation=45, ha='right', fontsize=12, color='white')
plt.yticks(fontsize=12, color='white')

plt.grid(True, axis='y', linestyle='--', alpha=0.3, color='white')
plt.legend([], [], frameon=False)
plt.tight_layout()
