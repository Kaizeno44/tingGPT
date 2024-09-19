from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = ''
CHATGPT_API_URL = 'https://api.openai.com/v1/chat/completions'
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
    try:
        response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except Exception as e:
        print(f"Lỗi khi gửi yêu cầu đến ChatGPT: {e}")
        return "Xin lỗi, có lỗi xảy ra khi xử lý yêu cầu."



@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data.get('message', {}).get('chat', {}).get('id')
    text = data.get('message', {}).get('text')

    if chat_id and text:
        reply = send_to_chatgpt(text)

        try:
            response = requests.post(
                f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
                json={'chat_id': chat_id, 'text': reply}
            )
            response.raise_for_status()  # Kiểm tra nếu có lỗi HTTP
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi gửi tin nhắn đến Telegram: {e}")
            return f"Lỗi khi gửi tin nhắn: {e}", 500
    else:
        return "Dữ liệu không hợp lệ", 400

    return '', 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)