import os
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

line_bot_api = LineBotApi('Pdt/ED1rOmznxrHueW+DLuKS/7jbqjwR+mU/vUyRBNxxmcmF+MD3omp03ROculxF2ziMKLIo5BwRWT9dwSKMMzApjKgPQCrVuF5yWkwcy9YL6B0Q4Turo9l8ydmbU59GNPT/8c16RspQQ31i4X1V/gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0802071f6bf26e330f0c61b392b0a5e2')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
