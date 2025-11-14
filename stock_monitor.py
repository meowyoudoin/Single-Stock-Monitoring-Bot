import yfinance as yf
import requests
from datetime import datetime

# --- CONFIGURATION ---
TICKER_SYMBOL = 'GOOGL'  # Example: Google Stock
ALERT_PRICE = 160.00     # The price threshold you want to monitor
WEBHOOK_URL = 'https://webhook.site/37d30ea8-e8fb-4314-bdde-62b9bd800bd5' 
# ---------------------

def fetch_and_check_price(ticker, threshold):
    """Fetches current price and checks against the threshold."""
    try:
        # 1. Fetch Data
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checked {ticker}: Current Price = ${current_price:.2f}")

        # 2. Monitoring Check (Condition)
        if current_price < threshold:
            alert_message = f"🚨 P1 ALERT: {ticker} price (${current_price:.2f}) has dropped BELOW the threshold of ${threshold:.2f}."
            print(f"!!! {alert_message}")
            
            # 3. Alerting (Webhook)
            send_webhook_alert(ticker, current_price, threshold, alert_message)
            
        else:
            print(f"Status OK: Price is above ${threshold:.2f}")

    except Exception as e:
        print(f"Error checking stock price for {ticker}: {e}")
        # Send an error webhook if the monitoring script itself fails
        send_error_webhook(f"Monitoring Script Failure for {ticker}: {e}")

def send_webhook_alert(ticker, price, threshold, message):
    """Sends a payload to the webhook for an alert."""
    payload = {
        "alert_source": "SimpleStockMonitorBot",
        "alert_time": datetime.now().isoformat(),
        "severity": "P1 - Critical",
        "ticker": ticker,
        "current_price": price,
        "threshold_breached": threshold,
        "action": "BUY_ALERT",
        "message": message
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status() # Raises an exception for bad status codes
        print(f"Webhook alert sent successfully. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

def send_error_webhook(error_message):
    """Sends a notification if the script encounters an operational error."""
    payload = {
        "alert_source": "Script_Operational_Failure",
        "alert_time": datetime.now().isoformat(),
        "severity": "P2 - Warning",
        "message": error_message
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except:
        pass # Silently fail if the error webhook itself fails

if __name__ == "__main__":
    fetch_and_check_price(TICKER_SYMBOL, ALERT_PRICE)