import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:***************@localhost:5432/postgres")

query = """
    SELECT 
        f.ticker,
        f.market_cap / 1000000000.0 AS market_cap_billions,
        s.sector
    FROM v_sp500_companies_fundamentals f
    JOIN comparison_by_sectors s
        ON f.ticker = s.ticker
    WHERE market_cap IS NOT NULL
    ORDER BY f.market_cap DESC
    LIMIT 20
"""
df = pd.read_sql(query, engine)
df_top20 = df.sort_values(by='market_cap_billions', ascending=False)

mean_market_cap = df_top20['market_cap_billions'].mean()
median_market_cap = df_top20['market_cap_billions'].median()

df_top20['moving_avg'] = df_top20['market_cap_billions'].rolling(window=3, min_periods=1).mean()

fig = px.bar(
    df_top20,
    x='ticker',
    y='market_cap_billions',
    title='Top 20 Companies by Market Capitalization (31.12.2024)',
    labels={'ticker': 'Company Ticker', 'market_cap_billions': 'Market Cap (Billion USD)'},
    text='market_cap_billions',
    hover_data=['sector']
)
fig.add_hline(
    y=mean_market_cap,
    line_dash="dash",
    line_color="cyan",
    annotation_text=f"Mean: {mean_market_cap:.2f} B USD",
    annotation_position="top right",
    annotation_font_color="white"
)
fig.add_hline(
    y=median_market_cap,
    line_dash="dot",
    line_color="magenta",
    annotation_text=f"Median: {median_market_cap:.2f} B USD",
    annotation_position="bottom right",
    annotation_font_color="white"
)
fig.add_trace(
    go.Scatter(
        x=df_top20['ticker'],
        y=df_top20['moving_avg'],
        mode='lines+markers',
        line=dict(color='lime'),
        name='Moving Average (3)'
    )
)
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside', selector=dict(type='bar'))

fig.update_layout(
    xaxis_title="Company Ticker",
    yaxis_title="Market Cap (Billion USD)",
    showlegend=True,
    bargap=0.2,
    template='plotly_dark',
    title_font=dict(size=18, color='white'),
    xaxis=dict(title_font=dict(size=14, color='white'), tickfont=dict(size=12, color='white')),
    yaxis=dict(title_font=dict(size=14, color='white'), tickfont=dict(size=12, color='white')),
    plot_bgcolor='#3c3c3c',
    paper_bgcolor='#333333'
)
fig.show()
