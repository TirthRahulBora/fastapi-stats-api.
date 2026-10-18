# FastAPI Descriptive Statistics Service

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Test:
```bash
curl "http://127.0.0.1:8000/stats?values=1,2,3"
```

## Deploy to Render

1. Push these files to a GitHub repository.
2. In Render, choose **New + → Blueprint** and select the repository containing `render.yaml`.
3. Deploy and copy the public service URL Render provides.
4. Test `/stats?values=1,2,3` and the CORS preflight before submitting the base URL.

Only `https://dash-rzuh37.example.com` is allowed as a CORS origin. All responses include `X-Request-ID` and `X-Process-Time`.
