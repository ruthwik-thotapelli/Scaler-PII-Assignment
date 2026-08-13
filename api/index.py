import os
import io
import sys
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from docx import Document

# Resolve directories
base_dir = os.path.dirname(os.path.abspath(__file__))
public_dir = os.path.join(base_dir, "public")

# Append api directory for redact_pii imports
sys.path.append(base_dir)
from redact_pii import redact_docx
import redact_pii

app = FastAPI(title="PII Redaction API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve UI Static Pages through FastAPI to guarantee no Vercel CDN 404s
@app.get("/")
def get_index():
    return FileResponse(os.path.join(public_dir, "index.html"))

@app.get("/style.css")
def get_css():
    return FileResponse(os.path.join(public_dir, "style.css"))

@app.get("/app.js")
def get_js():
    return FileResponse(os.path.join(public_dir, "app.js"))

# API routes
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "PII Redaction Engine"}

@app.post("/api/redact")
async def redact_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Unsupported format. Upload a .docx file.")
        
    try:
        contents = await file.read()
        input_stream = io.BytesIO(contents)
        output_stream = io.BytesIO()
        
        # Reset global mapping
        redact_pii.ENTITY_MAP.clear()
        
        # Process redaction
        redact_docx(input_stream, output_stream)
        output_stream.seek(0)
        
        encoded_file = base64.b64encode(output_stream.read()).decode("utf-8")
        
        return {
            "success": True,
            "filename": f"redacted_{file.filename}",
            "file_data": encoded_file,
            "mapping": dict(redact_pii.ENTITY_MAP)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
