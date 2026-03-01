from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/ebay-notifications", methods=["POST"])
def ebay_notifications():
    data = request.json
    print("Received notification:", data)
    return jsonify({"status": "received"}), 200

@app.route("/")
def home():
    return "eBay Notification Endpoint Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)