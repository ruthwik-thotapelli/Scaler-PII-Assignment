import os
import io
import sys
import base64
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from docx import Document

# Append the parent directory to sys.path so we can import redact_pii
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from redact_pii import redact_docx
import redact_pii

app = FastAPI(title="PII Redaction API")

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "PII Redaction Engine"}

@app.post("/api/redact")
async def redact_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a .docx file.")
        
    try:
        # Read the file to byte stream
        contents = await file.read()
        input_stream = io.BytesIO(contents)
        output_stream = io.BytesIO()
        
        # Reset the global ENTITY_MAP to ensure clean separation between requests
        redact_pii.ENTITY_MAP.clear()
        
        # Process redaction
        redact_docx(input_stream, output_stream)
        
        # Seek output stream to beginning for encoding
        output_stream.seek(0)
        
        # Base64 encode the output docx to return in the JSON response
        encoded_file = base64.b64encode(output_stream.read()).decode("utf-8")
        
        return {
            "success": True,
            "filename": f"redacted_{file.filename}",
            "file_data": encoded_file,
            "mapping": dict(redact_pii.ENTITY_MAP)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redaction failed: {str(e)}")
