import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf


# ===============================
# Load Market Data
# ===============================
def load_market_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)

    if data.empty:
        raise ValueError("No data fetched. Please check ticker or date range.")

    # Fix MultiIndex column issue (new yfinance versions)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.dropna()
    return data


# ===============================
# Backtesting Engine
# ===============================
class BacktestingEngine:
    def __init__(self, data, initial_capital=1_000_000, commission=0.001):
        self.data = data
        self.initial_capital = initial_capital
        self.cash = float(initial_capital)
        self.position = 0
        self.commission = commission
        self.trades = []
        self.portfolio_values = []

    def run_backtest(self):
        for i in range(1, len(self.data)):

            price = float(self.data["Close"].iloc[i])
            prev_signal = int(self.data["signal"].iloc[i - 1])
            current_signal = int(self.data["signal"].iloc[i])

            # Buy crossover
            if prev_signal == -1 and current_signal == 1:
                self.buy(price)

            # Sell crossover
            elif prev_signal == 1 and current_signal == -1:
                self.sell(price)

            portfolio_value = self.cash + self.position * price
            self.portfolio_values.append(portfolio_value)

        # Final portfolio value
        final_price = float(self.data["Close"].iloc[-1])
        return self.cash + self.position * final_price

    def buy(self, price):
        if self.position == 0:
            quantity = int(self.cash // price)

            if quantity <= 0:
                return

            cost = quantity * price
            commission_cost = cost * self.commission

            self.cash -= (cost + commission_cost)
            self.position = quantity

            self.trades.append(("BUY", price, quantity))

    def sell(self, price):
        if self.position > 0:
            quantity = self.position
            revenue = quantity * price
            commission_cost = revenue * self.commission

            self.cash += (revenue - commission_cost)
            self.position = 0

            self.trades.append(("SELL", price, quantity))

    # ===============================
    # Performance Metrics
    # ===============================
    def calculate_performance(self):

        if len(self.portfolio_values) < 2:
            return None

        portfolio_values = np.array(self.portfolio_values)

        returns = np.diff(portfolio_values) / portfolio_values[:-1]
        returns = returns[~np.isnan(returns)]

        total_return = (portfolio_values[-1] - self.initial_capital) / self.initial_capital
        annualized_return = (1 + total_return) ** (252 / len(self.data)) - 1

        volatility = np.std(returns) * np.sqrt(252)
        sharpe_ratio = (annualized_return - 0.02) / volatility if volatility != 0 else 0

        # Drawdown
        cumulative_max = np.maximum.accumulate(portfolio_values)
        drawdown = (portfolio_values - cumulative_max) / cumulative_max
        max_drawdown = np.min(drawdown)

        # Win Ratio
        profits = []
        for i in range(1, len(self.trades), 2):
            buy_price = self.trades[i - 1][1]
            sell_price = self.trades[i][1]
            qty = self.trades[i - 1][2]

            profit = (sell_price - buy_price) * qty
            profits.append(profit)

        win_ratio = (
            len([p for p in profits if p > 0]) / len(profits)
            if profits else 0
        )

        return {
            "Total Return": total_return,
            "Annualized Return": annualized_return,
            "Volatility": volatility,
            "Sharpe Ratio": sharpe_ratio,
            "Max Drawdown": max_drawdown,
            "Win Ratio": win_ratio
        }

    # ===============================
    # Plot Portfolio
    # ===============================
    def plot_results(self):
        if not self.portfolio_values:
            print("No portfolio values to plot.")
            return

        plt.figure(figsize=(12, 6))
        plt.plot(self.data.index[1:], self.portfolio_values)
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.show()


# ===============================
# Main Function
# ===============================
def main():
    print("=== SMA Crossover Backtesting System ===")

    symbol = input("Enter Ticker (e.g., AAPL, MSFT, TCS.NS): ")
    start_date = input("Start Date (YYYY-MM-DD): ")
    end_date = input("End Date (YYYY-MM-DD): ")

    data = load_market_data(symbol, start_date, end_date)

    # Calculate SMAs using pandas (more stable than ta)
    data["SMA_50"] = data["Close"].rolling(50).mean()
    data["SMA_200"] = data["Close"].rolling(200).mean()

    data = data.dropna()

    # Generate signals
    data["signal"] = np.where(data["SMA_50"] > data["SMA_200"], 1, -1)

    engine = BacktestingEngine(data)

    final_value = engine.run_backtest()

    performance = engine.calculate_performance()

    if performance:
        print("\n=== Performance Metrics ===")
        for key, value in performance.items():
            print(f"{key}: {value:.2%}")

    print(f"\nFinal Portfolio Value: ₹{final_value:,.2f}")

    engine.plot_results()


if __name__ == "__main__":
    main()