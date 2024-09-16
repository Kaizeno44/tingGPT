from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = ''
CHATGPT_API_URL = ''
CHATGPT_API_KEY = ''


def send_to_chatgpt(text):
    headers = {
        'Authorization': f'Bearer {CHATGPT_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': text}]
    }
    response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
    response_data = response.json()
    return response_data['choices'][0]['message']['content']


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']

    reply = send_to_chatgpt(text)
    requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', json={'chat_id': chat_id, 'text': reply})

    return '', 200


if __name__ == '__main__':
    app.run()
