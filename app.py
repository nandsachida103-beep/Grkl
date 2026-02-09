from flask import Flask, render_template, request, jsonify
from data import school_data, CONTACT

app = Flask(__name__)

BOT_NAME = "Sinoy"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").lower()

    # fees handling
    if "fee" in user_msg or "fees" in user_msg:
        for key in school_data:
            if "fee" in key and any(word in user_msg for word in key.split()):
                return jsonify({"reply": school_data[key]})

    # direct match
    for key, value in school_data.items():
        if key in user_msg:
            return jsonify({"reply": value})

    return jsonify({
        "reply": f"Sorry, I don’t have that info. Please contact school: {CONTACT['numbers']}"
    })


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
