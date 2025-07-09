# 🧠 AI-Powered Anomaly Detection for GRC & DORA Compliance

This project is an AI-powered anomaly detection tool designed for 'file access monitoring' in financial and GRC (Governance, Risk, and Compliance) environments. It uses machine learning to detect risky user behavior, such as odd-hour access, sensitive file downloads, and cross-department file misuse — helping organizations align with frameworks like ISO 27001, GDPR, and the 'EU DORA regulation'.

---

## 📦 Features

- 📁 Upload `.xlsx` or `.csv` files with user access data
- 🧠 Real-time anomaly detection using **Isolation Forest**
- 🔧 Automatic feature engineering (hour extraction, sensitivity encoding, dept mismatch)
- 📊 Displays top anomalies based on behavior patterns
- 💾 Download results with risk flags and anomaly scores

---

## 🗂️ File Structure

| File | Purpose |
|------|---------|
| `app.py` | Streamlit interface to run the detection system |
| `sample_anomaly_data.xlsx` | A sample dataset to test the app |
| `requirements.txt` | List of dependencies for local setup |

---

## ⚙️ How to Run Locally

### Step 1: Install Python and dependencies

```bash
pip install -r requirements.txt
