# Reading Helper — Frontend

Quick frontend using React + Vite. This is a minimal SPA that uploads a `.txt` file to the backend endpoint `/process-text` and renders annotated tokens.

Run (after installing Node.js):

```bash
cd frontend
npm install
npm run dev
```

Notes:
- Backend must be running at the host used by the fetch. The backend currently allows CORS from `*`, so `vite` dev server can call `/process-text` directly if you run the frontend from the repository root and proxy `/` to backend, or run the frontend and backend on the same host and port mapping.
- Example backend start:

```bash
cd backend
venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```
