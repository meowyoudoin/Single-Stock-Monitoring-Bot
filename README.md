# Single-Stock-Monitoring-Bot
Because who has time to monitor a full portfolio 🙈

# 🤖 Simple Stock Monitoring Bot (Python/SRE Showcase)

This project is a lightweight, automated stock monitoring bot built in Python. It simulates a **proactive operational health check** for a financial asset, leveraging automation and webhooks for immediate alerting when a critical threshold is breached.

It serves as a direct showcase of skills in **Python Scripting, Automation, and Proactive Monitoring/Alerting**—core competencies of a Site Reliability Engineer (SRE).

---

## ✨ Project Highlights & Skills Demonstrated

| Skill Area | Demonstration in Project |
| :--- | :--- |
| **Python Scripting** | Uses the `yfinance` library to fetch real-time stock data and the `requests` library to manage external API calls. |
| **Proactive Monitoring** | Implements a **threshold-based alerting rule** (If Price < $160.00, alert P1), demonstrating conditional checks crucial for system health monitoring. |
| **Operational Webhooks** | Sends a structured **JSON payload** to a real testing endpoint (`webhook.site`) when the price condition is met. This mimics triggering a P1 incident ticket or an immediate notification. |
| **Automation & Scheduling** | Includes a `run_monitor.sh` Bash script to automatically run the Python check every 5 minutes, simulating a scheduled job (e.g., Cron) for continuous monitoring. |
| **Error Handling** | Includes a `try...except` block to catch potential API or network errors, demonstrating the operational resilience needed to monitor the monitoring system itself. |

---

## 💻 Technical Stack

* **Python 3:** Core programming language.
* **`yfinance` Library:** Used to fetch financial market data (stock prices) without needing a registered API key.
* **`requests` Library:** Used to send HTTP POST requests (webhooks) to the alerting endpoint.
* **Bash Scripting:** Used for the simple execution loop (`run_monitor.sh`).