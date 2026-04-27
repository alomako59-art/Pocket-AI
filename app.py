import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Прямая проверка ключа
API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/chat')
def chat():
    user_text = request.args.get('text', 'Привет')
    
    # Если ключ забыли добавить в Environment Variables
    if not API_KEY:
        return "Ошибка: API ключ не настроен в настройках Render!"

    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": user_text}]
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://groq.com", 
                                 json=payload, headers=headers)
        # Если Groq ответил ошибкой, мы увидим её вместо 500
        if response.status_code != 200:
            return f"Groq Error: {response.text}"
            
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка сервера: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

