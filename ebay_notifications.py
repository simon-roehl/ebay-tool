import hashlib
import os
from flask import Flask, request, jsonify


app = Flask(__name__)

VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENDPOINT_URL = "https://ebay-tool.onrender.com/ebay-notifications"

@app.route("/ebay-notifications", methods=["GET", "POST"])
def ebay_notifications():

    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")
        if not challenge_code:
            return "Missing challenge_code", 400

        if not VERIFICATION_TOKEN:
            return "Verification token not configured", 500
        hash_input = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        challenge_response = hashlib.sha256(hash_input.encode()).hexdigest()

        return jsonify({
            "challengeResponse": challenge_response
        })

    if request.method == "POST":
        data = request.json
        print("Received account deletion notification:", data)
    # Future-proof placeholder
    # delete_user_data_if_exists(data)
        return "", 200