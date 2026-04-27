import os
from flask import Flask, request
from groq import Groq

app = Flask(__name__)

# Инициализируем клиента Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/chat')
def chat():
    user_query = request.args.get('text', '')
    
    if not user_query:
        return "Слушаю..."

    try:
        # Официальный способ запроса
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Ты краткий ассистент."},
                {"role": "user", "content": user_query},
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Ошибка Groq: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
