import requests
from openbb import obb
import os 
import time 
from datetime import datetime, timedelta
from symbols import symbols as stocks

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def is_overbought_rsi(rsi_values, threshold=70):
    """Check if RSI indicates the stock is overbought."""
    close_rsi_30 = rsi_values['close_RSI_30']
    return close_rsi_30[-1] > threshold

def is_overbought_stoch(stoch_values, threshold=75):
    """Check if Stochastic Oscillator indicates the stock is overbought.""" 
    close_stoch_30 = stoch_values['STOCHk_14_3_3']
    return close_stoch_30[-1] > threshold

def is_oversold_rsi(rsi_values, threshold=30):
    """Check if RSI indicates the stock is oversold."""
    close_rsi_30 = rsi_values['close_RSI_30']
    return close_rsi_30[-1] < threshold

def is_oversold_stoch(stoch_values, threshold=25):
    """Check if Stochastic Oscillator indicates the stock is oversold.""" 
    close_stoch_30 = stoch_values['STOCHk_14_3_3']
    return close_stoch_30[-1] < threshold



def send_discord_message(message):
    """Send a message to Discord."""
    data = {
        "content": message
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord: {response.status_code}, {response.text}")

def analyze_stocks(stocks):
    for stock in stocks:
        ticker = stock["ticker"]
        indicators = stock["indicators"]
        print(f"Analyzing {ticker} with indicators: {indicators}...")

        three_months_ago = datetime.now() - timedelta(days=90)
        start_date = three_months_ago.strftime('%Y-%m-%d')
        # Fetch historical price data
        try:
            stock_data = obb.equity.price.historical(symbol=ticker, start_date=start_date, provider='yfinance')
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            continue

        overbought_signals = []
        oversold_signals = []

        # Calculate RSI if included in indicators
        if "rsi" in indicators:
            rsi_data = obb.technical.rsi(data=stock_data.results, target='close', length=30, scalar=100.0, drift=1)

            rsi_results = rsi_data.to_dict()
            if is_overbought_rsi(rsi_results):
                overbought_signals.append("RSI")

            if is_oversold_rsi(rsi_results):
                oversold_signals.append("RSI")
                

        # Calculate Stochastic Oscillator if included in indicators
        if "stoch" in indicators:
            stoch_data = obb.technical.stoch(data=stock_data.results, fast_k_period=30, slow_d_period=6, slow_k_period=6)
            stoch_results = stoch_data.to_dict()
            if is_overbought_stoch(stoch_results):
                overbought_signals.append("Stochastic Oscillator")

            if is_oversold_stoch(stoch_results):
                oversold_signals.append("Stochastic Oscillator")

        # Output the results and send to Discord if overbought
        if overbought_signals:
            message = f"{ticker} is overbought based on: {', '.join(overbought_signals)}"

            send_discord_message(message)
        else:
            print(f"{ticker} is not overbought.")

        if oversold_signals:
            message = f"{ticker} is oversold based on: {', '.join(oversold_signals)}"

            send_discord_message(message)
        else:
            print(f"{ticker} is not oversold.")

if __name__ == "__main__":
    analyze_stocks(stocks)
