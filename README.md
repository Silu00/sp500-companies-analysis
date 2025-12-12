# S&P 500 Companies Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557c)

A comprehensive data analysis project focusing on the S&P 500 index. This repository contains scripts and notebooks to retrieve, process, and visualize financial data for the top 500 publicly traded companies in the U.S.

## Project Overview

The goal of this project is to provide insights into the U.S. stock market structure using historical data and fundamental metrics.

**Key Objectives:**
* **Data Acquisition:** Automated scraping of the current S&P 500 constituents (tickers, sectors, industries) from public sources (e.g., Wikipedia).
* **Financial Data Extraction:** Fetching historical stock prices and key financial metrics (Market Cap, P/E Ratio, Dividend Yield) using APIs (e.g., `yfinance`).
* **Sector Analysis:** Analyzing the distribution of companies across different sectors (Technology, Healthcare, Energy, etc.).
* **Visualization:** Creating intuitive charts to display market trends, correlations, and distributions.

## Features

* **Automated Ticker Scraping:** Keeps the list of companies up-to-date.
* **Sector & Industry Breakdown:** Visual representation of market dominance by sector.
* **Correlation Matrix:** Analyzes how different stocks move in relation to each other.
* **Risk vs. Return:** scatter plots identifying high-growth/high-risk assets.
* **Market Cap Distribution:** Analysis of the size disparity between mega-cap companies and the rest of the index.

## Technologies Used

* **Python:** Core programming language.
* **Pandas & NumPy:** For efficient data manipulation and aggregation.
* **Yfinance:** For downloading historical market data.
* **Pandas `read_html`:** For scraping the constituents table.
* **Matplotlib & Seaborn:** For static and statistical data visualization.
