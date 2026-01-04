# AI Interview Preparation Agent

Streamlit app for practicing data-science interview questions using Google Gemini (via `google-genai`).

Files:
- `app.py` — Streamlit app entry
- `interview_agent.py` — (if present) supporting agent code
- `requirements.txt` — Python dependencies

How to run locally (venv):

```powershell
python -m venv venv
& venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Deploy to Streamlit Community Cloud:
1. Push this repository to GitHub and publish the branch.
2. On Streamlit Community Cloud, click "New app" → connect your GitHub repo → select branch and folder.
3. Add the environment variable `GEMINI_API_KEY` under "Advanced settings" → "Secrets".
4. Deploy.
