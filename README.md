# 🤖 Simple Stock Monitoring Bot (SRE Operational Showcase)

This project is a resilient, automated stock monitoring bot built in Python. It serves as a direct showcase of **Site Reliability Engineering (SRE) principles** by integrating proactive, multi-channel alerting, state management for cooldowns, and backtesting for reliability analysis.

---

## ✨ Project Highlights & SRE Skills Demonstrated

| SRE Principle / Skill | Demonstration in Project |
| :--- | :--- |
| **Proactive Monitoring** | Implements a **threshold-based alerting rule** (e.g., If Price < $160.00, alert P1), crucial for monitoring system health and business metrics. |
| **Operational Alerting (Multi-Channel)** | Alerts are distributed via two robust channels: **Real-time Webhook** (for system integration/incident ticket) and **SMTP Email** (for direct user/stakeholder notification). |
| **State Management & Cooldown** | Uses a local **`monitor_state.json`** file to track the last alert time, implementing a **24-hour cooldown** period. This prevents alert spam and ensures operational stability. |
| **Backtesting & Analysis** | Includes a dedicated function to run the monitoring logic against **historical stock data**, demonstrating the ability to perform reliability analysis and test alerting rules offline. |
| **Python Scripting** | Uses `yfinance`, `requests`, and built-in libraries (`json`, `smtplib`) to handle data fetching, persistence, and external communications. |

---

## 💻 Technical Stack

* **Python 3:** Core programming language.
* **`yfinance`:** Used to fetch real-time and historical financial market data.
* **`requests`:** Used to send HTTP POST requests (Webhooks).
* **`smtplib`:** Python's built-in library used for sending secure email notifications (SMTP).
* **`json` / `os`:** Used for local file-based **State Management**.
* **Webhook.site:** Used as a temporary, live destination to confirm successful webhook delivery.

---

## ⚙️ Setup and Configuration

### Prerequisites

You need **Python 3** and the following libraries installed:

```bash
pip install yfinance requests