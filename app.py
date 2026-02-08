from flask import Flask, request, jsonify
from data import SCHOOL_DATA, CONTACT

app = Flask(__name__)
BOT_NAME = "Sinoy"


def find_answer(user_msg):
    user_msg = user_msg.lower()

    # Direct match from data.py
    for key, value in SCHOOL_DATA.items():
        if key in user_msg:
            return value

    return (
        "Sorry, I don’t have this information right now. "
        f"Please contact the school office at {CONTACT['numbers']}."
    )


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Gurukul Convent School AI",
        "chatbot": BOT_NAME
    })


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    if not user_msg:
        return jsonify({"reply": f"{BOT_NAME}: Please ask a valid question."})

    answer = find_answer(user_msg)
    return jsonify({"reply": f"{BOT_NAME}: {answer}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
