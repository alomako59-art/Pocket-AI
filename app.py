import os
from flask import Flask, request
import requests
import urllib.parse  # Добавили для обработки текста

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/chat', methods=['GET'])
def chat():
    # Получаем сырой текст и декодируем его правильно
    user_query = request.args.get('text', '')
    
    if not user_query:
        return "Я тебя слушаю. Задай свой вопрос."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Ты крутой ИИ помощник в приложении Pocket Code. Отвечай кратко, понятно и по делу."},
            {"role": "user", "content": user_query}
        ]
    }

    try:
        response = requests.post("https://groq.com", 
                                 json=data, headers=headers)
        result = response.json()
        return result['choices']['message']['content']
    except Exception:
        return "Упс, ошибка связи с мозгом! Проверь интернет."

if __name__ == '__main__':
    # Порт для Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
