def find_answer(user_msg):
    user_msg = user_msg.lower().strip()

    # Exact + partial key matching
    for key, value in SCHOOL_DATA.items():
        if key in user_msg or user_msg in key:
            return value

    # Extra: handle class fee variations
    if "fee" in user_msg or "fees" in user_msg:
        for key, value in SCHOOL_DATA.items():
            if "fee" in key and any(word in user_msg for word in key.split()):
                return value

    # Fallback
    return (
        "Sorry, I don’t have this information right now. "
        f"Please contact the school office at {CONTACT['numbers']}."
    )
