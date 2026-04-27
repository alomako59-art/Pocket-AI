import os
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/chat', methods=['POST']) # Теперь только POST
def chat():
    # Получаем JSON данные из Pocket Code
    data = request.get_json(force=True)
    user_query = data.get('text', '')
    
    if not user_query:
        return "Пустой запрос", 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Ты краткий ассистент на русском языке."},
                {"role": "user", "content": user_query},
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices.message.content
    except Exception as e:
        return f"Ошибка Groq: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)


