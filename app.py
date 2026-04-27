import os
from flask import Flask, request
import requests

app = Flask(__name__)
API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/chat', methods=['GET'])
def chat():
    user_text = request.args.get('text', 'Привет')
    
    if not API_KEY:
        return "Ошибка: Ключ GROQ_API_KEY не найден в Environment Variables!"

    # Ссылка для Groq
    url = "https://groq.com"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Ты краткий ИИ-помощник."},
            {"role": "user", "content": user_text}
        ]
    }

    try:
        # Явно указываем POST запрос к Groq
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices']['message']['content']
        else:
            return f"Groq Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Ошибка сервера: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
