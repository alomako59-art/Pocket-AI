import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Берем ключ из настроек сервера (безопасно)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/chat', methods=['GET'])
def chat():
    user_query = request.args.get('text', '')
    if not user_query:
        return "Я тебя не слышу"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Ты краткий и полезный ИИ помощник в приложении Pocket Code."},
            {"role": "user", "content": user_query}
        ]
    }

    try:
        response = requests.post("https://groq.com", 
                                 json=data, headers=headers)
        result = response.json()
        return result['choices']['message']['content']
    except Exception as e:
        return "Ошибка связи с ИИ"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
