from flask import Flask, request, jsonify
import openai
import os

# Set your OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

app = Flask(__name__)
MEMORY_FILE = 'memory.txt'

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def save_to_memory(user_msg, ai_response):
    with open(MEMORY_FILE, 'a', encoding='utf-8') as f:
        f.write(f"User: {user_msg}\nAI: {ai_response}\n\n")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data['message']
    
    # Load previous memory
    previous_context = load_memory()
    prompt = f"{previous_context}User: {user_message}\nAI:"

    # Call ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or gpt-4 if you have access
        messages=[
            {"role": "system", "content": "You are a super-intelligent assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    ai_reply = response['choices'][0]['message']['content'].strip()

    # Save to memory
    save_to_memory(user_message, ai_reply)

    return jsonify({'response': ai_reply})

if __name__ == '__main__':
    app.run(debug=True)
