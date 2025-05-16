import os
from flask import Flask, request, jsonify, render_template
import pyttsx3
import speech_recognition as sr
import requests

app = Flask(__name__)

# Initialize pyttsx3 for Text-to-Speech (TTS)
engine = pyttsx3.init()

# Function to generate a response from Ollama (Llama 3.2)
def generate_response(input_text):
    url = "http://localhost:11434/api/generate"  # Default Ollama API endpoint
    payload = {
        "model": "llama3.2",  # Ensure the correct model name
        "prompt": input_text,
        "stream": False
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "No response generated.")
    return "Error generating response."

# Function to convert speech to text using SpeechRecognition
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for speech...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing speech...")
        speech_text = recognizer.recognize_google(audio)
        return speech_text
    except sr.UnknownValueError:
        return "Could not understand the speech."
    except sr.RequestError:
        return "Error with the speech service."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/voice-agent', methods=['POST'])
def voice_agent():
    user_input = speech_to_text()
    response = generate_response(user_input)
    return jsonify({
        "user_input": user_input,
        "response": response
    })

@app.route('/text-agent', methods=['POST'])
def text_agent():
    data = request.json
    user_input = data.get("text_input", "")
    response = generate_response(user_input)
    return jsonify({
        "user_input": user_input,
        "response": response
    })

if __name__ == '__main__':
    app.run(debug=True)
