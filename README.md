# 🤖 InstaReply Bot

A fine-tuned AI chatbot that generates professional replies to Instagram-style social media comments. 

🚀 **Live Web App**: [insta-reply-bot.streamlit.app](https://insta-reply-bot-byzf6nmx2yudkiwgzyncyc.streamlit.app/)

Runs entirely on your machine locally or online via free cloud hosting — no APIs, no cloud costs.

**Model**: FLAN-T5-Small (~77M parameters, ~300 MB on disk)  
**Training**: CPU-only, ~30–60 minutes  
**Inference**: 1–3 seconds per reply on CPU

---

## Quick Start

### 1. Create a virtual environment

```bash
cd insta-reply-bot
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the training dataset

```bash
python generate_dataset.py
```

This creates ~1,000 comment→reply pairs in `data/train.json` and `data/val.json`.

### 4. Train the model

```bash
python train.py
```

This fine-tunes FLAN-T5-Small on the generated dataset. Takes ~30–60 minutes on CPU.  
The trained model is saved to `model/insta-reply-flan-t5/`.

**Optional flags:**
```bash
python train.py --epochs 3 --batch-size 2 --learning-rate 5e-4
```

### 5. Run the chatbot

```bash
python reply.py
```

You'll see an interactive prompt:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🤖 InstaReply Bot
  Type a comment to get a reply suggestion.
  Commands: 'quit' to exit, 'clear' to clear screen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Paste comment: Love this product!

✨ Reply: Thank you so much for your kind words! We really appreciate your support. 😊
   (1.2s)

💬 Paste comment: What's the price?

✨ Reply: Thanks for your interest! Please check the link in our bio for pricing details, or send us a DM and we'll be happy to help.
   (1.4s)
```

**Single-comment mode** (non-interactive):
```bash
python reply.py --comment "This is amazing!"
```

---

## Project Structure

```
insta-reply-bot/
├── generate_dataset.py   # Create the training dataset
├── train.py              # Fine-tune FLAN-T5-Small
├── reply.py              # Interactive chatbot CLI
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── data/
│   ├── train.json        # Training data (~900 pairs)
│   └── val.json          # Validation data (~100 pairs)
└── model/
    └── insta-reply-flan-t5/  # Saved fine-tuned model (~300 MB)
```

---

## How It Works

1. **Dataset**: `generate_dataset.py` creates ~1,000 curated comment→reply pairs across 5 categories (compliments, questions, feedback, engagement, generic).

2. **Training**: `train.py` fine-tunes Google's FLAN-T5-Small model on this dataset. FLAN-T5 is a Seq2Seq model designed for "input→output" tasks, making it ideal for "comment→reply" generation.

3. **Inference**: `reply.py` loads the fine-tuned model and runs an interactive loop where you paste comments and get professional reply suggestions.

---


---

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'transformers'` | Run `pip install -r requirements.txt` |
| `Model not found` error in reply.py | Run `python train.py` first |
| Training runs out of memory | Reduce batch size: `python train.py --batch-size 2` |
| Slow training | Expected — CPU training takes 30–60 min. Be patient! |
| Poor reply quality | Try more epochs: `python train.py --epochs 8` |
