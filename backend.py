"""
backend.py — FastAPI server for the RAG pipeline
══════════════════════════════════════════════════════

This replaces Streamlit with a proper REST API so our
custom HTML frontend can talk to the RAG pipeline.

Two endpoints:
  POST /build  → Upload files, build FAISS index
  POST /query  → Ask a question, get an answer

Run with:
    pip install fastapi uvicorn python-multipart
    uvicorn backend:app --reload --port 8000

Then open frontend.html in your browser.
"""

import os
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag_pipeline import RAGPipeline

# ── App setup ─────────────────────────────────────────────────
app = FastAPI(title="College RAG API", version="1.0.0")

# Allow the frontend HTML file to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # In production, set to your domain
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend HTML at /
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("frontend.html")

# ── Global RAG instance (persists between requests) ───────────
rag_instance: RAGPipeline | None = None
UPLOAD_DIR = Path("temp_uploads")


# ══════════════════════════════════════════════════════════════
#  POST /build  — Upload files and build FAISS index
# ══════════════════════════════════════════════════════════════
@app.post("/build")
async def build_index(
    api_key:       str = Form(...),
    chunk_size:    int = Form(500),
    chunk_overlap: int = Form(50),
    files: List[UploadFile] = File(...),
):
    """
    Accepts uploaded files, runs the full RAG ingestion pipeline,
    and returns the number of chunks created.
    """
    global rag_instance

    # Save uploaded files to disk temporarily
    UPLOAD_DIR.mkdir(exist_ok=True)
    file_paths = []

    for f in files:
        path = UPLOAD_DIR / f.filename
        with open(path, "wb") as buf:
            shutil.copyfileobj(f.file, buf)
        file_paths.append(str(path))

    try:
        # Build the RAG pipeline
        rag = RAGPipeline(
            api_key=api_key,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        num_chunks = rag.build_index(file_paths)
        rag_instance = rag   # Store globally for /query calls

        return {
            "status": "success",
            "num_chunks": num_chunks,
            "num_files": len(files),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════════════════════════════
#  POST /query  — Ask a question
# ══════════════════════════════════════════════════════════════
class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query(req: QueryRequest):
    """
    Given a question, retrieves relevant chunks and returns
    a Gemini-generated answer grounded in your documents.
    """
    if rag_instance is None:
        raise HTTPException(
            status_code=400,
            detail="No index built yet. Call /build first."
        )

    try:
        answer, sources = rag_instance.query(req.question)
        return {
            "answer": answer,
            "sources": sources,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Health check ──────────────────────────────────────────────
@app.get("/health")
def health():
    return {
        "status": "ok",
        "indexed": rag_instance is not None,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
