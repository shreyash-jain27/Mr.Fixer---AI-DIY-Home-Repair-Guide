from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# ✅ Use authenticated Hugging Face model
MODEL_NAME = "meta-llama/Llama-2-7b-chat-hf"

try:
    chatbot = pipeline("text-generation", model=MODEL_NAME)
    print("✅ AI Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading AI Model: {e}")
    chatbot = None


@app.route("/")
def home():
    return jsonify({"message": "Welcome to Mr. Fixer - AI DIY Home Repair Guide!"})

# ✅ AI Chatbot Route


@app.route("/chat", methods=["POST"])
def chat():
    if chatbot is None:
        return jsonify({"error": "AI model failed to load"}), 500

    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        # AI Model Processing
        response = chatbot(
            f"Provide a step-by-step DIY repair guide for: {user_message}", max_length=200, truncation=True)
        ai_response = response[0]['generated_text']
    except Exception as e:
        ai_response = "Sorry, I couldn't process your request."

    return jsonify({"response": ai_response})


if __name__ == "__main__":
    app.run(debug=True)
