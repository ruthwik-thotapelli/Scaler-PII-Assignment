import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI(title="PII Redaction API Mock")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = os.path.dirname(os.path.abspath(__file__))
public_dir = os.path.join(base_dir, "public")

@app.get("/")
def get_index():
    return FileResponse(os.path.join(public_dir, "index.html"))

@app.get("/style.css")
def get_css():
    return FileResponse(os.path.join(public_dir, "style.css"))

@app.get("/app.js")
def get_js():
    return FileResponse(os.path.join(public_dir, "app.js"))

@app.get("/mock_redacted.docx")
def get_mock_docx():
    return FileResponse(os.path.join(public_dir, "mock_redacted.docx"))

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "PII Redaction Engine (Mock)"}

@app.post("/api/redact")
async def redact_file(file: UploadFile = File(...)):
    # This route is bypassed by app.js, but included for completeness
    return JSONResponse({"status": "bypassed"})
