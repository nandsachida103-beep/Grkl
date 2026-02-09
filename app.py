from flask import Flask, render_template, request, jsonify
from data import school_data, CONTACT

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    # sort keys by length (important fix)
    sorted_keys = sorted(school_data.keys(), key=len, reverse=True)

    for key in sorted_keys:
        if key in user_message:
            return jsonify({
                "chatbot": "Sinoy",
                "message": school_data[key]
            })

    return jsonify({
        "chatbot": "Sinoy",
        "message": f"Sorry, I don’t have this information right now. Please contact the school office at {CONTACT['numbers']}."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
