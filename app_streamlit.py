import streamlit as st
import torch
import time
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# Set page config for a premium experience
st.set_page_config(
    page_title="InstaReply AI — Web Dashboard",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS for Premium Glassmorphism Aesthetics ───────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    /* Main body background */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f8fafc;
    }
    
    /* Title styling */
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }
    
    /* Custom Glassmorphic Card */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }
    
    /* Header branding */
    .header-logo {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
    }
    
    .avatar-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        border-radius: 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 22px;
        color: white;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
    }
    
    /* Status indicator */
    .status-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
    
    .status-dot {
        width: 6px;
        height: 6px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10b981;
    }
    
    /* Custom Output box */
    .output-box {
        background: rgba(15, 23, 42, 0.4);
        border: 1px dashed rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
    }
    
    /* Button modifications */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        width: 100%;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45) !important;
    }
    
    /* Text Area custom styling */
    textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# ── Header Section ────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-logo">
    <div class="avatar-icon">🤖</div>
    <div>
        <h1 style="margin: 0; font-size: 26px;">InstaReply AI</h1>
        <div class="status-badge"><span class="status-dot"></span> Cloud Engine Online</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Load Model (Cached to avoid reload on user input) ─────────────────────────
MODEL_NAME = "Jennie10/insta-reply-bot"

@st.cache_resource(show_spinner="📦 Loading model from Hugging Face Hub (this takes ~30 seconds on first run)...")
def load_model():
    # Limit CPU threads to avoid latency issues
    torch.set_num_threads(2)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

try:
    tokenizer, model = load_model()
except Exception as e:
    st.error(f"Error loading model from Hugging Face: {e}")
    st.info("Make sure the model files have finished uploading completely.")
    st.stop()

# ── Main Card ─────────────────────────────────────────────────────────────────
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.subheader("💬 Input Instagram Comment")

comment_input = st.text_area(
    label="Comment",
    placeholder="Paste a comment here to generate a reply...",
    height=120,
    label_visibility="collapsed"
)

# Character Counter
if comment_input:
    st.markdown(f"<div style='text-align: right; font-size: 12px; color: #94a3b8; margin-top: -10px;'>{len(comment_input)} characters</div>", unsafe_allow_html=True)

st.write("") # Spacer

if st.button("✨ Generate Suggested Reply"):
    if not comment_input.strip():
        st.warning("Please type or paste a comment first!")
    else:
        start_time = time.time()
        
        with st.spinner("🤖 Thinking..."):
            try:
                # Format prompt
                input_text = f"Reply to this Instagram comment: {comment_input}"
                inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True)
                
                # Generate
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
                
                # Output suggestion
                st.markdown(f"""
                <div class="output-box">
                    <strong style="color: #10b981; font-size: 14px;"><i class="fa-solid fa-reply"></i> Suggested Reply</strong>
                    <p style="font-size: 16px; margin-top: 10px; line-height: 1.6; color: #f8fafc;">{reply}</p>
                    <div style="font-size: 11px; color: #94a3b8; margin-top: 15px;">
                        ⏱️ Generated in {elapsed:.2f} seconds
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Inference Error: {e}")

st.markdown('</div>', unsafe_allow_html=True)
