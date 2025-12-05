from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import socket

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyCXEW1vbTCUj8LqKxDJL8s_qSXe80X3HN4"  
MODEL_NAME = "gemini-2.5-flash"
BOT_NAME = "Rishabh"

client = genai.Client(api_key=API_KEY)

def internet_available(host="8.8.8.8", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception:
        return False

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")

    if not internet_available():
        msg = user_msg.lower()
        if any(w in msg for w in ["hello", "hi", "good"]):
            bot_reply = "Hi! I am Rishabh, your support assistant."
        elif "your name" in msg:
            bot_reply = "I am Rishabh, your chatbot."
        elif any(w in msg for w in ["help", "refund"]):   
            bot_reply = "Yes please describe the issue, I'm here to help you"
        else:
            bot_reply = "Sorry, I am in demo mode. Please check your internet connection."
        return jsonify({"reply": bot_reply, "bot_name": BOT_NAME})



    try:
        result = client.models.generate_content(
            model=MODEL_NAME,
            contents=user_msg
        )
        bot_reply = result.text
        return jsonify({"reply": bot_reply})
    except Exception as e:
        msg = user_msg.lower()
        if "hello" in msg:
            bot_reply = "Hi! I am Rishabh, your support assistant."
        elif "your name" in msg:
            bot_reply = "I am Rishabh, your chatbot."
        else:
            bot_reply = "Sorry, I am in demo mode. Please check your internet connection."

        return jsonify({"reply": bot_reply, "bot_name": BOT_NAME})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
