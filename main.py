from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi('5OpClASIe7+VGcheUVYzx6dVHp9q3FYIvCcN2BoNfgmGkNbZE64T/ffVao8y3z52efnJQ5Z+3KkM+r8et6WfjJbNkcfqkYQT2pwN4UR1bOZ940kY8DdKSviLRNXKQk5/Deq7R9wd/NKRUMcgKBzgZwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5033959d062d929efa452602b1a29efc')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    for i in range(10):
        line_bot_api.reply_message(reply_token, TextSendMessage(text = message))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)