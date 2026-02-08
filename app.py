from flask import Flask, request, jsonify
from data import SCHOOL_DATA, school_data, CONTACT

app = Flask(__name__)
BOT_NAME = "Sinoy"


def search_nested(data, user_msg):
    """Recursively search in nested dictionary/list"""
    if isinstance(data, dict):
        for key, value in data.items():
            if key.lower().replace("_", " ") in user_msg:
                return value
            result = search_nested(value, user_msg)
            if result:
                return result

    elif isinstance(data, list):
        for item in data:
            result = search_nested(item, user_msg)
            if result:
                return result

    return None


def handle_fees(user_msg):
    # Nursery / LKG / UKG
    if "nursery" in user_msg:
        return "Nursery fee is ₹500 per month."
    if "lkg" in user_msg:
        return "LKG fee is ₹550 per month."
    if "ukg" in user_msg:
        return "UKG fee is ₹600 per month."

    # Class 1–12
    for i in range(1, 13):
        if f"class {i}" in user_msg or f"class{i}" in user_msg:
            fee = school_data["fee_structure"].get(str(i))
            if fee:
                return f"Class {i} fee is ₹{fee} per month."

    return SCHOOL_DATA.get("class 11 fee")


def find_answer(user_msg):
    user_msg = user_msg.lower()

    # 1️⃣ Exact match from flat SCHOOL_DATA
    for key, value in SCHOOL_DATA.items():
        if key in user_msg:
            return value

    # 2️⃣ Fee handling
    if "fee" in user_msg or "fees" in user_msg:
        return handle_fees(user_msg)

    # 3️⃣ Timing
    if "timing" in user_msg or "time" in user_msg:
        return SCHOOL_DATA.get("school timing")

    # 4️⃣ Teachers
    if "teacher" in user_msg or "sir" in user_msg or "mam" in user_msg:
        teachers = school_data["senior_teachers"]
        reply = "Senior teachers are:\n"
        for name, subject in teachers.items():
            reply += f"- {name} ({subject})\n"
        return reply.strip()

    # 5️⃣ Transport
    if "transport" in user_msg or "bus" in user_msg:
        return SCHOOL_DATA.get("transport")

    # 6️⃣ Sports
    if "sport" in user_msg or "game" in user_msg:
        return SCHOOL_DATA.get("sports")

    # 7️⃣ Monitor
    if "monitor" in user_msg:
        for key in SCHOOL_DATA:
            if "monitor" in key and key in user_msg:
                return SCHOOL_DATA[key]

    # 8️⃣ Admission
    if "admission" in user_msg or "document" in user_msg:
        return SCHOOL_DATA.get("documents required")

    # 9️⃣ Science exhibition
    if "science" in user_msg or "exhibition" in user_msg:
        return (
            SCHOOL_DATA.get("science exhibition date") + " " +
            SCHOOL_DATA.get("head of science exhibition")
        )

    # 🔟 Search in structured school_data
    nested_result = search_nested(school_data, user_msg)
    if nested_result:
        return str(nested_result)

    # ❌ Fallback
    return (
        "Sorry, I don’t have this information right now. "
        f"Please contact the school office at {CONTACT['numbers']}."
    )


@app.route("/", methods=["GET"])
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
