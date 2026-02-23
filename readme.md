# 📈 Quantitative Trading Strategy & Market Analytics Dashboard

## 📌 Overview

This project combines quantitative trading strategy development in Python with interactive financial visualization in Power BI. It implements a 50/200 Simple Moving Average (SMA) crossover strategy, performs full backtesting with risk metrics, and presents structured market insights through a dashboard.

The objective is to analyze historical market behavior, evaluate strategy performance, and understand risk-adjusted returns using real stock data from Yahoo Finance.

---

## 🛠️ Tech Stack

- **Python**
  - pandas
  - numpy
  - matplotlib
  - yfinance
- **Power BI**
- Financial Metrics & Backtesting Logic

---

## 📊 Data Source

- Historical stock data fetched using **Yahoo Finance API** via `yfinance`
- OHLC data (Open, High, Low, Close, Volume)
- User-defined ticker and date range

---

## ⚙️ Strategy Logic

### 50/200 SMA Crossover Strategy

- 50-day SMA represents short-term trend  
- 200-day SMA represents long-term trend  
- Buy signal → When SMA 50 crosses above SMA 200  
- Sell signal → When SMA 50 crosses below SMA 200  

This is a trend-following strategy commonly used in financial markets.

---

## 🧮 Backtesting Engine

The backtesting system simulates:

- Buy/Sell trades  
- Commission deduction  
- Capital allocation  
- Portfolio value tracking  
- Trade logging  

Final portfolio value is calculated at the end of the test period.

---

## 📈 Performance Metrics Calculated

- Total Return  
- Annualized Return  
- Volatility (annualized)  
- Sharpe Ratio (risk-adjusted return)  
- Maximum Drawdown  
- Win Ratio  

These metrics help evaluate both profitability and risk exposure.

---

## 📊 Power BI Dashboard

The dashboard includes:

- Candlestick chart (OHLC visualization)  
- Sector-based filtering  
- Date-range filtering  
- Historical price trend analysis  
- Structured market behavior visualization  

It complements the Python backtesting by providing intuitive visual insights.

---

## 🚀 How to Run the Python Project

### 1️⃣ Install Dependencies

```bash
pip install pandas numpy matplotlib yfinance

### 2️⃣ Run the Script

```bash
python your_script_name.py

### 3️⃣ Enter:

```bash
Ticker (e.g., AAPL, MSFT, TCS.NS)

Start Date (YYYY-MM-DD)

End Date (YYYY-MM-DD)

You will see:

Strategy performance metrics

Final portfolio value

Portfolio growth chart


## 🎯 Project Objective

- Evaluate the effectiveness of a trend-following strategy  
- Understand risk-adjusted performance  
- Simulate realistic trading with commissions  
- Analyze market behavior through visualization  
- Build a structured financial research workflow  

---

## ⚠️ Disclaimer

This project is for educational and research purposes only and does not constitute financial advice. All trading strategies involve risk.