import os
import dotenv
from flask import Flask, request, abort
from pyngrok import ngrok
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage
)

from server import ask_ai, clear_history, get_history_count

dotenv.load_dotenv()

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))

HISTORY_FILE = "chat_history.json"


@app.route("/callback", methods=["POST"])
def callback():

    signature = request.headers["X-Line-Signature"]

    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    user_id = event.source.user_id
    mtext = event.message.text.strip()

    try:

        # ===== 系統指令 =====

        if mtext == "@清除記憶":

            clear_history(user_id)

            reply = (
                "已清除聊天記錄\n"
                "之後的對話將重新開始。"
            )

        elif mtext == "@記憶狀態":

            count = get_history_count(user_id)

            reply = (
                f"目前已保存 {count} 筆聊天記錄"
            )

        elif mtext == "@幫助":

            reply = (
                "可使用指令：\n\n"
                "@記憶狀態\n"
                "查看目前保存的聊天數量\n\n"
                "@清除記憶\n"
                "清除所有聊天記錄\n\n"
                "其他任何訊息都會交給 AI 回答"
            )

        # ===== AI問答 =====

        else:

            reply = ask_ai(
                user_id=user_id,
                user_message=mtext
            )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )

    except Exception as e:

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text=f"系統發生錯誤：\n{str(e)}"
            )
        )


if __name__ == "__main__":
    
    public_url = ngrok.connect(5000)
    ngrok_url = str(public_url).split(' -> ')[0].replace('NgrokTunnel: "', '').replace('"', '')
    print(ngrok_url)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )