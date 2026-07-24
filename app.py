#!/usr/bin/env python3
"""
app.py — Local FastAPI backend that loads the fine-tuned T5 model and
serves the interactive web dashboard.

Usage:
    python app.py
"""

import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import uvicorn

# ── Setup and Constants ──────────────────────────────────────────────────────

app = FastAPI(title="InstaReply AI Local Server")

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "insta-reply-flan-t5")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Ensure static folder exists
os.makedirs(STATIC_DIR, exist_ok=True)

# ── Load Model ───────────────────────────────────────────────────────────────

print()
print("━" * 60)
print("  🤖 Loading InstaReply AI Model...")
print("━" * 60)

if not os.path.exists(MODEL_PATH):
    print(f"❌ Error: Fine-tuned model not found at {MODEL_PATH}")
    print("   Please train the model first by running: python train.py")
    sys.exit(1)

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)
    model.eval()
    print("  ✅ Model loaded successfully and ready!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    sys.exit(1)

# ── API Endpoint ──────────────────────────────────────────────────────────────

class CommentRequest(BaseModel):
    comment: str

class ReplyResponse(BaseModel):
    reply: str
    elapsed: float

@app.post("/api/reply", response_model=ReplyResponse)
def get_reply(data: CommentRequest):
    import time
    start_time = time.time()
    
    try:
        input_text = f"Reply to this Instagram comment: {data.comment}"
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True)
        
        # Generate output using beam search configuration
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_new_tokens=100,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3,
        )
        
        reply = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        elapsed = time.time() - start_time
        
        return ReplyResponse(reply=reply, elapsed=elapsed)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

# ── Serve Dashboard (Static Files) ───────────────────────────────────────────

# Mount the static files directory to serve our HTML dashboard at the root URL
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# ── Startup Runner ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Optimize CPU threads for PyTorch to prevent context switching latency on startup
    import torch
    torch.set_num_threads(2)
    
    print()
    print("  🌐 Starting web dashboard at: http://localhost:8000")
    print("  Press Ctrl+C to stop the server.")
    print("━" * 60)
    print()
    
    # Run the server locally on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
