from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('jfH8WzUZ0r7vx+zXVjmbNw5tjUTQPrZpq0irncFIAhUnjzdahALrwiSrh0SIR8Iwy21rXowG46L9hU0c+aVCWyY45ebBadzx+niHyavfmsrBNe2t7JGI3XB0m8mO8n+srcTyvsffqEslQQNT+v0ihQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1c769522a05d5734c206695ca3f92e62')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()