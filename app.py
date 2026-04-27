import os
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/chat', methods=['GET'])
def chat():
    # Получаем вопрос из Pocket Code
    user_query = request.args.get('text', 'Привет')
    
    # Твой ключ из настроек Render
    api_key = os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        return "Ошибка: API ключ не найден в настройках Render!"

    # Прямой запрос к Groq
    url = "https://groq.com"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "Ты помощник в Pocket Code. Отвечай очень кратко."},
            {"role": "user", "content": user_query}
        ]
    }

    try:
        # Отправляем запрос и ждем ответа
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices']['message']['content']
        else:
            # Если Groq ругается, он скажет почему
            return f"Groq вернул ошибку {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Ошибка при запросе: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
