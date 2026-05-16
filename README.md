# Bharti Connect — Billing API & Knowledge Base

A production-ready FastAPI backend and premium Knowledge Base for telecom billing demonstrations.

## 🚀 Key Features
- **FastAPI Backend**: 7 modular endpoints for invoices, usage history, balance, activation logs, credits, and ticketing.
- **Mock Data Baseline**: Pre-loaded with 12 months of history for multiple users, normalized to **May 2026**.
- **Auto-Reset Logic**: Built-in state management (`seed.py`) that ensures a clean "Day 0" state on every restart.
- **Premium Knowledge Base**: AI-crawlable, SEO-friendly HTML/CSS static site inspired by Airtel's design system.
- **Production Ready**: Optimized for deployment on Render and exposure via ngrok.

## 📁 Project Structure
```text
bharti-connect-api/
├── app/
│   ├── main.py          # Entry point & static file mounting
│   ├── seed.py          # Data seeding & reset logic
│   └── routers/
│       ├── crm.py       # Billing, Usage, Balance & Credit endpoints
│       └── ticketing.py # Support ticket creation endpoints
├── data/                # Persistent JSON storage (Auto-seeded)
├── knowledge_base/      # Static HTML/CSS site (served at /kb)
├── requirements.txt     # Python dependencies
├── render.yaml          # Render deployment config
└── runtime.txt          # Python version pinning (3.12.0)
```

## 🛠️ Local Setup

1. **Clone & Navigate**:
   ```bash
   git clone https://github.com/purusottamsingh-create/bharti-connect.git
   cd bharti-connect
   ```

2. **Setup Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run Server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🌐 Access Points
- **API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Knowledge Base**: [http://127.0.0.1:8000/kb/](http://127.0.0.1:8000/kb/)
- **Health Check**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## 🧪 Demo Data
- **Test Mobile Numbers**: `9876543210`, `7406179387`, `9858509904`
- **Baseline Date**: May 15, 2026
- **Reset Trigger**: Simply restart the server to restore all JSON files to their original state.

## ☁️ Deployment
This repository is pre-configured for **Render**. Connect your GitHub account and it will automatically build using the provided `render.yaml`.
