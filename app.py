from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
from flask import Flask, request, abort

app = Flask(__name__)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('LINE_CHANNEL_SECRET')

line_bot_api = LineBotApi(channel_access_token)
line_handler = WebhookHandler(channel_secret)

# Webhook endpoint
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        line_handler.handle(body, signature)
    except Exception as e:
        print(e)
        abort(400)
    return 'OK'

# 事件處理器
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='你說了: ' + event.message.text)
    )

if __name__ == "__main__":
    app.run()
