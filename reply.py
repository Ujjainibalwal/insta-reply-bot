#!/usr/bin/env python3
"""
reply.py — Interactive CLI chatbot for generating Instagram comment replies.

Loads the fine-tuned FLAN-T5-Small model and runs an interactive REPL where
you paste Instagram comments and get professional reply suggestions.

Usage:
    python reply.py
    python reply.py --model-path ./model/insta-reply-flan-t5
"""

import argparse
import os
import sys
import time

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# ── Constants ────────────────────────────────────────────────────────────────

DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "insta-reply-flan-t5")
INPUT_PREFIX = "Reply to this Instagram comment: "

# Generation parameters tuned for short, professional replies
GENERATION_CONFIG = {
    "max_new_tokens": 100,
    "num_beams": 4,
    "early_stopping": True,
    "no_repeat_ngram_size": 3,
    "temperature": 0.8,
    "do_sample": False,  # Use beam search for consistent, professional outputs
}


# ── Model Loading ────────────────────────────────────────────────────────────

def load_model(model_path: str):
    """Load the fine-tuned model and tokenizer from disk."""
    if not os.path.exists(model_path):
        print(f"❌ Error: Model not found at: {model_path}")
        print()
        print("   You need to train the model first. Run these commands:")
        print("   1. python generate_dataset.py")
        print("   2. python train.py")
        print()
        sys.exit(1)

    # Check for key model files
    config_file = os.path.join(model_path, "config.json")
    if not os.path.exists(config_file):
        print(f"❌ Error: No config.json found in {model_path}")
        print("   The model directory appears incomplete. Try re-running train.py.")
        sys.exit(1)

    print("📦 Loading model... ", end="", flush=True)
    start = time.time()

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    model.eval()

    elapsed = time.time() - start
    print(f"done ({elapsed:.1f}s)")

    return model, tokenizer


# ── Reply Generation ─────────────────────────────────────────────────────────

def generate_reply(comment: str, model, tokenizer) -> str:
    """Generate a professional reply to an Instagram comment."""
    # Format the input the same way as training data
    input_text = f"{INPUT_PREFIX}{comment}"

    # Tokenize
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=128,
        truncation=True,
    )

    # Generate
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        **GENERATION_CONFIG,
    )

    # Decode
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply.strip()


# ── Interactive REPL ─────────────────────────────────────────────────────────

def run_repl(model, tokenizer):
    """Run the interactive comment→reply loop."""
    print()
    print("━" * 50)
    print("  🤖 InstaReply Bot")
    print("  Type a comment to get a reply suggestion.")
    print("  Commands: 'quit' to exit, 'clear' to clear screen")
    print("━" * 50)
    print()

    while True:
        try:
            comment = input("💬 Paste comment: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            break

        # Handle commands
        if not comment:
            continue
        if comment.lower() in ("quit", "exit", "q"):
            print("\n👋 Goodbye!")
            break
        if comment.lower() == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        # Generate reply
        start = time.time()
        try:
            reply = generate_reply(comment, model, tokenizer)
            elapsed = time.time() - start

            print()
            print(f"✨ Reply: {reply}")
            print(f"   ({elapsed:.1f}s)")
            print()

        except Exception as e:
            print(f"\n❌ Error generating reply: {e}\n")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="InstaReply Bot — Generate professional Instagram comment replies"
    )
    parser.add_argument(
        "--model-path",
        type=str,
        default=DEFAULT_MODEL_PATH,
        help=f"Path to the fine-tuned model directory (default: {DEFAULT_MODEL_PATH})",
    )
    parser.add_argument(
        "--comment",
        type=str,
        default=None,
        help="Generate a single reply to this comment and exit (non-interactive mode)",
    )
    args = parser.parse_args()

    # Load model
    model, tokenizer = load_model(args.model_path)

    # Non-interactive mode: single comment
    if args.comment:
        reply = generate_reply(args.comment, model, tokenizer)
        print(reply)
        return

    # Interactive mode: REPL
    run_repl(model, tokenizer)


if __name__ == "__main__":
    main()
