# Bharti Connect API

A FastAPI backend application providing mock billing data, configured for easy deployment on Render.

## Project Structure

```
bharti-connect-api/
├── app/
│   ├── main.py          ← FastAPI app entry point
│   ├── mock_data.py     ← 12 months of mock invoice data
│   └── routers/
│       └── billing.py   ← GET /billing/invoices endpoint
├── requirements.txt
├── render.yaml          ← Render auto-deploy config
└── README.md
```

## Running Locally

1. Setup a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

4. View the interactive API documentation at:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Deployment

This project includes a `render.yaml` for automatic deployment to Render. Simply connect your GitHub repository to Render and it will automatically provision the service.
