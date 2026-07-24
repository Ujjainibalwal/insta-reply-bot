#!/usr/bin/env python3
"""
generate_dataset.py — Generate a curated training dataset for Instagram comment replies.

Creates ~1,000 comment→reply pairs across 5 categories:
  1. Compliments (~250 pairs)
  2. Questions (~250 pairs)
  3. Feedback/Complaints (~150 pairs)
  4. Engagement (~150 pairs)
  5. Generic/Short (~200 pairs)

Output: data/train.json (90%) and data/val.json (10%)

Usage:
    python generate_dataset.py
"""

import json
import os
import random

# Reproducible results
random.seed(42)

INPUT_PREFIX = "Reply to this Instagram comment: "

# ── Category 1: Compliments ──────────────────────────────────────────────────

COMPLIMENT_COMMENTS = [
    "Love this!", "Amazing post!", "Beautiful 😍", "So inspiring!",
    "Best page ever", "This is goals", "Absolutely stunning",
    "You always post the best content", "So gorgeous!", "I'm obsessed with this",
    "Such a great post!", "Incredible work", "Love the vibe here",
    "Always killing it!", "This made my day", "Wow this is everything",
    "Can't stop looking at this", "You never disappoint!", "Pure perfection",
    "This is art 🎨", "My favorite page!", "Soooo pretty", "Just wow",
    "I live for your posts", "Keep slaying!", "Chef's kiss 🤌",
    "You're the best!", "This is fire 🔥", "Phenomenal work here",
    "I screenshot this for inspo", "Flawless as always", "Major inspo 💫",
    "I wish I could double-like this", "Goals goals goals",
    "This just made my morning", "Literal perfection", "Outstanding!",
    "Why is every post so good?", "How do you do it every time?",
    "I'm in love with this aesthetic", "Can't get enough of your content",
    "Your page is a mood", "This deserves a million likes",
    "Top tier content right here", "Absolutely breathtaking!",
    "I shared this with everyone I know", "This post wins the internet today",
    "Your content is always so fresh", "Wow just incredible",
    "You have the best taste", "I aspire to this level",
]

COMPLIMENT_REPLIES = [
    "Thank you so much! We really appreciate the kind words.",
    "Thanks for the love! So glad you enjoyed it. 😊",
    "We appreciate you! Thanks for being part of our community.",
    "Thank you! Your support means the world to us.",
    "So happy to hear that! Thanks for stopping by.",
    "Thanks! We love sharing this with you.",
    "Appreciate the kind feedback! Have a wonderful day.",
    "Thank you! Stay tuned for more content like this.",
    "Thanks for the compliment! We always try our best.",
    "You're too kind! Thanks for the support.",
    "That truly means a lot to us. Thank you!",
    "So glad you like it! More great content is on the way.",
    "Thank you for the wonderful feedback! It motivates us to keep going.",
    "Wow, thank you! Comments like yours make our day. 😊",
    "We're so grateful for your support! Thank you.",
    "Thank you! We put a lot of thought into every post.",
    "Hearing this makes all the effort worthwhile. Thanks!",
    "We're blushing! Thank you so much for the kind words.",
    "Your support fuels us to keep creating. Thank you!",
    "Thanks! We love hearing from amazing followers like you.",
    "So glad this resonated with you! Thanks for sharing.",
    "Thank you! We're always looking to bring our best.",
    "We're thrilled you enjoy our content. Stay tuned!",
    "Your kind words really made our day. Thank you! 🌟",
    "Thank you for being such an awesome part of our community!",
]

# ── Category 2: Questions ────────────────────────────────────────────────────

QUESTION_COMMENTS = [
    "What's the price?", "Where can I buy?", "Is this available?",
    "How long does shipping take?", "Do you ship internationally?",
    "What sizes do you have?", "Are there other colors?",
    "When will this restock?", "How do I order?", "Can I get a discount code?",
    "Is this on sale?", "What material is this made from?",
    "How do I contact customer support?", "Do you accept returns?",
    "What's the return policy?", "Can I customize this?",
    "Is this handmade?", "How long does delivery take?",
    "Do you have a physical store?", "Can you ship to Europe?",
    "Is this limited edition?", "How do I place a bulk order?",
    "What payment methods do you accept?", "Any promo codes available?",
    "Where are you located?", "Is this product vegan/cruelty-free?",
    "What's the weight of this item?", "Does this come with a warranty?",
    "Can I pay with PayPal?", "When is the next drop?",
    "Do you do gift wrapping?", "How do I track my order?",
    "Is this true to size?", "What's the difference between the two versions?",
    "Can I get this personalized?", "How many are left in stock?",
    "Where is this manufactured?", "Any plans for a new collection?",
    "Do you ship to India?", "Can I pick up in store?",
    "Is free shipping available?", "What are the dimensions?",
    "How should I care for this item?", "Do you offer express shipping?",
    "Can I exchange instead of return?", "Is this suitable for kids?",
]

QUESTION_REPLIES = [
    "Hi! Please check the link in our bio for all pricing and availability details.",
    "Hello! You can find all the information on our website linked in our bio.",
    "Hi there! Please send us a DM and we'd be happy to help with your inquiry.",
    "Hello! All details are available on our website. Feel free to check it out!",
    "Hi! We offer a variety of options on our site. Browse via the link in our bio.",
    "Hello! Shipping details and policies are on our FAQ page. Check our bio link!",
    "Hi! Please sign up for our newsletter to get updates on restocks and promotions.",
    "Hello! Our customer service team can assist you. Please send us a DM!",
    "Hi there! You can purchase directly through our website linked in our bio.",
    "Hello! Feel free to DM us if you need help finding the right option.",
    "Great question! All the details are on our product page. Link in bio!",
    "Hi! We'd love to help. Send us a direct message with your specific question.",
    "Thanks for asking! You'll find the answer on our FAQ page. Link in our bio.",
    "Hi! Yes, we'd be happy to assist. Please reach out via DM for personalized help.",
    "Hello! For the most up-to-date info, please visit our website. Link in bio!",
    "Great question! Please DM us and our team will get back to you right away.",
    "Hi there! All product details including sizing are on our website.",
    "Thanks for your interest! We're happy to help — just send us a DM. 😊",
    "Hello! Please check our website for the most current availability and details.",
    "Hi! Our team would love to assist you. Drop us a message anytime!",
    "Thanks for reaching out! Full details are available on our site. Bio link!",
    "Hi there! We'd love to help you out. Please DM us your question!",
    "Great question! Our FAQ covers this in detail. Check the link in our bio.",
    "Hi! Everything you need is on our website. Don't hesitate to DM us too!",
]

# ── Category 3: Feedback / Complaints ────────────────────────────────────────

COMPLAINT_COMMENTS = [
    "Shipping was slow", "Quality could be better", "Not what I expected",
    "Customer service was unhelpful", "My item arrived damaged",
    "Still haven't received my order", "The sizing is way off",
    "Disappointed with my purchase", "Never shopping here again",
    "Very poor experience overall", "The color looks different from the photo",
    "Package was missing items", "Waited 3 weeks for delivery",
    "I've been trying to reach support for days", "The quality doesn't match the price",
    "Worst purchase I've made", "Asked for a refund but no response",
    "Product broke after one use", "False advertising honestly",
    "Not worth the money at all", "I regret buying this",
    "Your website glitched and charged me twice", "Packaging was terrible",
    "Got the wrong item entirely", "Very misleading product description",
    "Would not recommend to anyone", "Really let down by this",
    "Expected much better quality", "Don't waste your money people",
    "Had to return it immediately", "Terrible communication from your team",
]

COMPLAINT_REPLIES = [
    "We're so sorry to hear about your experience. Please DM us your order number so we can make this right.",
    "Apologies for the inconvenience. We'd love to look into this for you — please send us a direct message.",
    "We apologize that this didn't meet your expectations. Please reach out via DM so we can assist you.",
    "We're sorry for the frustration. Our team is here to help — please message us directly with your details.",
    "This isn't the standard we aim for. Please DM us so we can resolve this issue for you.",
    "We apologize for the delay and any trouble caused. Please send us a DM with your order info.",
    "We're sorry you had a negative experience. Please contact our support team via DM so we can help.",
    "Thank you for the feedback. We apologize for the issue and would like to fix it — please DM us.",
    "We're sorry to hear this. We take this seriously and would like to help if you message us.",
    "Apologies for the inconvenience caused. Let us help you resolve this via direct message.",
    "We completely understand your frustration. Please DM us and we'll prioritize your case.",
    "That's not acceptable and we sincerely apologize. Our team wants to make this right — please DM us.",
    "We're truly sorry about this experience. Please share your order details via DM and we'll act on it immediately.",
    "Thank you for letting us know. We want to fix this for you. Please reach out via DM with your details.",
    "We hear you and we're sorry. Customer satisfaction is our top priority. Please DM us so we can help.",
    "We apologize for falling short. Please send us a DM and we'll get this sorted out promptly.",
    "This is not the experience we want for our customers. Please DM us — we'll make it right.",
    "We're very sorry about this. Please reach out to us directly so we can resolve this as soon as possible.",
]

# ── Category 4: Engagement ───────────────────────────────────────────────────

ENGAGEMENT_COMMENTS = [
    "Can you follow back?", "Tag me!", "Check my page",
    "Collab?", "DM me", "Shoutout?", "Follow for follow?",
    "Let's collaborate!", "Check out my latest post", "Support each other?",
    "Please follow me back", "Hey can we work together?",
    "Looking for brand ambassadors?", "I'm an influencer, let's connect",
    "Hit me up for collab!", "Check your DMs please",
    "Like my recent?", "Can you feature me?", "S4S?",
    "Wanna partner up?", "Go see my page you'll love it",
    "Follow me I follow back", "Share for share?",
    "I just followed you, follow back?", "Would love a shoutout 🙏",
    "Can you repost my content?", "Let me be your brand rep!",
    "I'd love to work with your brand", "Visit my profile please",
    "L4L? F4F?", "Let's grow together!",
]

ENGAGEMENT_REPLIES = [
    "Thanks for reaching out! We appreciate you engaging with our content.",
    "Thanks for stopping by! Hope you're having a great day.",
    "Hello! Thanks for being active in our community.",
    "Hi there! We appreciate the comment and support.",
    "Thanks for connecting with us here!",
    "Hello! Always great to see our community engaging.",
    "Thanks for checking out our page! Have a wonderful day.",
    "Hi! Thanks for the comment, we appreciate it.",
    "Hello there! Thanks for engaging with our post.",
    "Thanks for reaching out! We value your support.",
    "We appreciate your enthusiasm! Thanks for being part of our community.",
    "Hi! Thank you for showing interest. We appreciate the engagement!",
    "Thanks for your support! We love our engaged community.",
    "Hi there! We appreciate you taking the time to comment.",
    "Thanks for being here! Our community means everything to us.",
    "Hello! Thanks for the kind energy. Have a great day!",
    "We appreciate the interest! Thanks for being part of our journey.",
    "Hi! Thanks for engaging. We love connecting with our followers!",
]

# ── Category 5: Generic / Short ──────────────────────────────────────────────

GENERIC_COMMENTS = [
    "First!", "🔥🔥🔥", "❤️", "Nice", "Wow", "💯", "Cool",
    "Awesome", "Great", "🙌", "Love", "Epic", "Yesss", "Perfect", "👏",
    "💪", "Insane", "Dope", "Lit", "Vibes", "Yes!!", "😍😍",
    "🫶", "So good", "Facts", "💕", "On point", "Nailed it", "🤩",
    "Obsessed", "Iconic", "Slay", "W", "❤️‍🔥", "Yooo", "10/10",
    "🙏", "Legendary", "Mood", "Crazy good", "No cap",
    "This", "Underrated", "Smooth", "Clean", "💎",
]

GENERIC_REPLIES = [
    "Thanks! Have a great day.",
    "Appreciate it!",
    "Thanks for the support!",
    "Glad you like it!",
    "Thank you!",
    "Thanks for stopping by!",
    "Hope you're having a good one!",
    "Appreciate the love!",
    "Thanks for commenting!",
    "Right back at you! Thanks!",
    "Cheers! Thanks for the love.",
    "Thank you for the support! 😊",
    "We appreciate you!",
    "Thanks! More to come!",
    "Love the energy! Thank you.",
    "You're awesome! Thanks!",
    "Thanks for being here!",
    "Glad this resonated with you!",
]


# ── Dataset Generation ───────────────────────────────────────────────────────

def generate_pairs(comments: list, replies: list, count: int, category: str) -> list:
    """Generate `count` comment→reply pairs with variety."""
    pairs = []
    for i in range(count):
        # Cycle through comments and replies to maximize coverage
        comment = comments[i % len(comments)]
        reply = replies[i % len(replies)]

        # Add some randomness after first full cycle
        if i >= min(len(comments), len(replies)):
            comment = random.choice(comments)
            reply = random.choice(replies)

        pairs.append({
            "input": f"{INPUT_PREFIX}{comment}",
            "output": reply,
            "category": category,  # Metadata — stripped before saving
        })
    return pairs


def main():
    """Generate and save the training dataset."""
    print()
    print("━" * 50)
    print("  📊 InstaReply Bot — Dataset Generator")
    print("━" * 50)
    print()

    # Create output directory
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    # Generate pairs per category
    categories = {
        "Compliments":  (COMPLIMENT_COMMENTS,  COMPLIMENT_REPLIES,  250),
        "Questions":    (QUESTION_COMMENTS,    QUESTION_REPLIES,    250),
        "Complaints":   (COMPLAINT_COMMENTS,   COMPLAINT_REPLIES,   150),
        "Engagement":   (ENGAGEMENT_COMMENTS,  ENGAGEMENT_REPLIES,  150),
        "Generic":      (GENERIC_COMMENTS,     GENERIC_REPLIES,     200),
    }

    all_pairs = []
    print("📝 Generating pairs:")
    for cat_name, (comments, replies, count) in categories.items():
        pairs = generate_pairs(comments, replies, count, cat_name)
        all_pairs.extend(pairs)
        print(f"   {cat_name:15s}  {count:4d} pairs  ({len(comments)} comments × {len(replies)} replies)")

    total = len(all_pairs)
    print(f"   {'─' * 40}")
    print(f"   {'Total':15s}  {total:4d} pairs")
    print()

    # Shuffle
    random.shuffle(all_pairs)

    # Strip category metadata before saving
    clean_pairs = [{"input": p["input"], "output": p["output"]} for p in all_pairs]

    # Split 90/10
    split_idx = int(total * 0.9)
    train_data = clean_pairs[:split_idx]
    val_data = clean_pairs[split_idx:]

    # Save
    train_path = os.path.join(data_dir, "train.json")
    val_path = os.path.join(data_dir, "val.json")

    with open(train_path, "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=2, ensure_ascii=False)

    with open(val_path, "w", encoding="utf-8") as f:
        json.dump(val_data, f, indent=2, ensure_ascii=False)

    print(f"💾 Saved:")
    print(f"   Train: {train_path} ({len(train_data)} pairs)")
    print(f"   Val:   {val_path} ({len(val_data)} pairs)")
    print()
    print("━" * 50)
    print("  ✅ Dataset generated! Run 'python train.py' next.")
    print("━" * 50)
    print()


if __name__ == "__main__":
    main()
