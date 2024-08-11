from openai import OpenAI
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key from .env
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Initialize Flask app
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat_post():
    data = request.json

    image_urls = data.get('image_urls', [])
    prompt = data.get('prompt', '')

    # Prepare messages for OpenAI API
    messages = [
        {"role": "user", "content": {"type": "text", "text": prompt}},
    ]

    for url in image_urls:
        messages.append(
            {"role": "user", "content": {"type": "image_url", "image_url": {"url": url}}}
        )

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
    )

    return jsonify(response.choices[0].message["content"])

@app.route('/api', methods=['GET'])
def chat_get():
    prompt = request.args.get('prompt')

    # Prepare the message for OpenAI API
    messages = [
        {"role": "user", "content": {"type": "text", "text": prompt}},
    ]

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
    )

    return jsonify(response.choices[0].message["content"])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
