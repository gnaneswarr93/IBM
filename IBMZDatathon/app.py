from flask import Flask, request, jsonify, render_template
from models.work import generate_response, log_conversation, get_past_conversations

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_reply = generate_response(user_message)
    log_conversation(user_message, bot_reply)
    return jsonify({"reply": bot_reply})

@app.route("/past_conversations", methods=["GET"])
def past_conversations():
    conversations = get_past_conversations()
    return jsonify({"conversations": conversations})

if __name__ == "__main__":
    app.run(debug=True)
