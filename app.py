import os
from flask import Flask, request
import requests

app = Flask(__name__)
API_KEY = os.environ.get("GROQ_API_KEY")

@app.route('/chat')
def chat():
    # Проверка: видит ли сервер ключ вообще?
    if not API_KEY:
        return "ОШИБКА: Сервер не видит переменную GROQ_API_KEY в настройках Render!"
    
    user_text = request.args.get('text', 'test')
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": user_text}]
    }

    try:
        r = requests.post("https://groq.com", 
                          json=payload, headers=headers)
        
        # Если Groq ответил не 200, выводим причину
        if r.status_code != 200:
            return f"Groq Error {r.status_code}: {r.text}"
            
        return r.json()['choices']['message']['content']
    except Exception as e:
        return f"Ошибка кода: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
