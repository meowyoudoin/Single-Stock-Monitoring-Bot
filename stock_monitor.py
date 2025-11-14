import yfinance as yf
import requests
import json
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# -------------------------------------
# ⚙️ CONFIGURATION
# -------------------------------------

# Stock & Monitoring Settings
TICKER_SYMBOL = 'GOOGL'         # The stock to monitor
ALERT_PRICE = 160.00            # The price threshold that triggers a P1 alert
STATE_FILE = 'monitor_state.json'
ALERT_RESET_HOURS = 24          # Cooldown period for the same alert (prevents spam)

# Webhook Settings
WEBHOOK_URL = 'https://webhook.site/37d30ea8-e8fb-4314-bdde-62b9bd800bd5' 

# Email Settings (Fill in to enable email alerting!)
USER_EMAIL = 'recipient@example.com'  # The email address to receive alerts
SENDER_EMAIL = 'your_sending_email@gmail.com' 
SENDER_PASSWORD = 'your_app_password' # IMPORTANT: Use an App Password, NOT your main password!
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
# -------------------------------------


# -------------------------------------
# 💾 STATE MANAGEMENT FUNCTIONS
# -------------------------------------

def load_state():
    """Loads the monitoring state from the local JSON file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: State file is corrupted. Starting with a fresh state.")
            return {"last_alert_time": None, "last_price": None}
    return {"last_alert_time": None, "last_price": None}

def save_state(state):
    """Saves the current monitoring state to the local JSON file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=4)
    except IOError as e:
        print(f"Error saving state file: {e}")


# -------------------------------------
# 🔔 ALERTING FUNCTIONS (Unified)
# -------------------------------------

def send_webhook_alert(payload):
    """Sends a payload to the webhook."""
    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status() # Raises an exception for bad status codes
        print(f"Webhook alert sent successfully. Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

def send_email_alert(recipient_email, subject, body):
    """Sends an email alert using standard SMTP."""
    # Skip if email credentials are not configured
    if not SENDER_PASSWORD or not SENDER_EMAIL or SENDER_EMAIL == 'your_sending_email@gmail.com':
        print("Email not configured. Skipping email alert.")
        return

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"Email alert sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
        print("Tip: Check network/firewall, and verify 'App Password' is correct.")

def send_alert(ticker, price, threshold, message, user_email):
    """Unified alerting function (Webhook + Email)."""
    # 1. Webhook Payload
    payload = {
        "alert_source": "SimpleStockMonitorBot",
        "alert_time": datetime.now().isoformat(),
        "severity": "P1 - Critical",
        "ticker": ticker,
        "current_price": price,
        "threshold_breached": threshold,
        "message": message
    }
    send_webhook_alert(payload)

    # 2. Email Alert
    email_subject = f"P1 ALERT: {ticker} Price Breach!"
    email_body = f"{message}\n\nTimestamp: {datetime.now().isoformat()}"
    send_email_alert(user_email, email_subject, email_body)


# -------------------------------------
# 📈 CORE MONITORING LOGIC
# -------------------------------------

def fetch_and_check_price(ticker, threshold, user_email):
    """Fetches current price, checks condition, and handles alerting/state."""
    state = load_state()
    current_time = datetime.now()
    
    try:
        # 1. Fetch Data
        stock = yf.Ticker(ticker)
        current_price = stock.history(period="1d")['Close'].iloc[-1]
        
        print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Checked {ticker}: Current Price = ${current_price:.2f}")

        # 2. Monitoring Check (Condition)
        if current_price < threshold:
            alert_message = f"🚨 P1 ALERT: {ticker} price (${current_price:.2f}) has dropped BELOW the threshold of ${threshold:.2f}."

            # Check for alert cooldown (State Management)
            if state['last_alert_time']:
                last_alert_dt = datetime.fromisoformat(state['last_alert_time'])
                
                # Check if we are within the cooldown period
                if current_time < last_alert_dt + timedelta(hours=ALERT_RESET_HOURS):
                    print(f"Status OK: Alert condition met, but still within {ALERT_RESET_HOURS}-hour cooldown.")
                    save_state(state) # Save state with current price, but skip alert
                    return

            # --- ALERT TRIGGERED (outside cooldown) ---
            print(f"!!! {alert_message}")
            send_alert(ticker, current_price, threshold, alert_message, user_email)

            # Update and save state after successful alert
            state['last_alert_time'] = current_time.isoformat()
            state['last_price'] = current_price
            save_state(state)
            
        else:
            # If price is normal, only update the last known price
            state['last_price'] = current_price
            save_state(state)
            print(f"Status OK: Price is above ${threshold:.2f}")

    except Exception as e:
        print(f"Error checking stock price for {ticker}: {e}")
        # Operational Alert: Send an error webhook if the monitoring script itself fails
        send_alert_error(f"Monitoring Script Failure for {ticker}: {e}")


def send_alert_error(error_message):
    """Sends a notification if the script encounters an operational error (P2)."""
    # This is a P2 alert for monitoring system health
    payload = {
        "alert_source": "Script_Operational_Failure",
        "alert_time": datetime.now().isoformat(),
        "severity": "P2 - Warning",
        "message": error_message
    }
    try:
        # Only send webhook for system error, skip email to keep it clean
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
    except:
        pass # Silently fail if the error webhook itself fails


# -------------------------------------
# 📊 BACKTESTING SIMULATION LOGIC
# -------------------------------------

def backtest_monitor(ticker, threshold, start_date, end_date):
    """Runs the monitoring logic against historical data."""
    print(f"\n--- Starting Backtest for {ticker} from {start_date} to {end_date} ---")
    
    # 1. Fetch Historical Data
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
    except Exception as e:
        print(f"Error fetching backtesting data: {e}")
        return

    # 2. Loop and Monitor
    alert_days = 0
    for date, row in data.iterrows():
        close_price = row['Close']
        
        # Apply the monitoring logic (no state/cooldown needed for backtesting)
        if close_price < threshold:
            alert_days += 1
            print(f"🚨 BACKTEST ALERT on {date.date()}: Price (${close_price:.2f}) was below threshold ${threshold:.2f}.")
            
    print(f"\n--- Backtest Complete ---")
    print(f"Total trading days checked: {len(data)}")
    print(f"Total days an alert would have triggered: {alert_days}")


# -------------------------------------
# 🚀 MAIN EXECUTION
# -------------------------------------

if __name__ == "__main__":
    
    # 1. Run Live Monitor Check
    fetch_and_check_price(TICKER_SYMBOL, ALERT_PRICE, USER_EMAIL)

    # 2. Run Backtest Example (Uncomment to execute)
    # backtest_monitor(TICKER_SYMBOL, ALERT_PRICE, "2024-01-01", "2024-03-01")

    # Note: To enable email, you must provide valid credentials in the CONFIGURATION section.