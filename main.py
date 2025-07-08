# emotional_support_app/main.py
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from transformers import pipeline
import os, json

app = Flask(__name__)
sentiment_pipeline = pipeline("sentiment-analysis")

# Create logs directory
if not os.path.exists("logs"):
    os.makedirs("logs")

def save_journal_entry(entry, sentiment):
    today = datetime.now().strftime("%Y-%m-%d")
    entry_data = {
        "date": today,
        "entry": entry,
        "sentiment": sentiment,
    }
    with open(f"logs/{today}.json", "w") as f:
        json.dump(entry_data, f)

def get_affirmation(sentiment_label):
    affirmations = {
        "POSITIVE": [
            "You're doing amazing! Keep it up!",
            "You're stronger than you think.",
            "Today is full of possibilities."
        ],
        "NEGATIVE": [
            "It's okay to feel down. This too shall pass.",
            "Be kind to yourself, you're doing your best.",
            "Take a deep breath. You're not alone."
        ]
    }
    return affirmations.get(sentiment_label, ["You're doing great!"])[0]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/journal", methods=["POST"])
def journal():
    data = request.json
    entry = data.get("entry")
    sentiment = sentiment_pipeline(entry)[0]
    save_journal_entry(entry, sentiment)
    affirmation = get_affirmation(sentiment['label'])
    return jsonify({"sentiment": sentiment, "affirmation": affirmation})

if __name__ == "__main__":
    app.run(debug=True)
