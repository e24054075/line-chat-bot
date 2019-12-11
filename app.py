import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage,TextSendMessage,ImageMessage,ImageSendMessage

from fsm import TocMachine
from utils import send_text_message,send_image_url

load_dotenv()

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

machine = {}
machine["0"] = TocMachine(
            states=["home", "mapinfo", "information"],
            transitions=[
                {
                    "trigger": "mapinfo_request",
                    "source": "home",
                    "dest": "mapinfo",
                },
                {
                    "trigger": "infor_request",
                    "source": "home",
                    "dest": "information",
                },
                {
                        "trigger": "go_back", 
                        "source": ["mapinfo","information"], 
                        "dest": "home",
                },
            ],
            initial="home",
            auto_transitions=False,
            show_conditions=False,
        )
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    '''app.logger.info("Request body: " + body)'''

    # parse webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    if user_id not in machine:
        machine[user_id] = TocMachine(
            states=["home", "mapinfo", "information"],
            transitions=[
                {
                    "trigger": "mapinfo_request",
                    "source": "home",
                    "dest": "mapinfo",
                },
                {
                    "trigger": "infor_request",
                    "source": "home",
                    "dest": "information",
                },
                {
                        "trigger": "go_back", 
                        "source": ["mapinfo","information"], 
                        "dest": "home",
                },
            ],
            initial="home",
            auto_transitions=False,
            show_conditions=False,
        )
    if(machine[user_id].is_home()):
        if event.message.text == "活動攻略":
            machine[user_id].mapinfo_request(event)
        elif event.message.text == "情報":
            machine[user_id].infor_request(event)
        elif event.message.text == "help":
            send_text_message(event.reply_token, "活動攻略:取得本次活動攻略\n情報:各情報網站網址")
        else:
            send_text_message(event.reply_token, "錯誤指令，如有需要請輸入help")
    elif(machine[user_id].is_mapinfo()):
        if event.message.text == "E1":
            send_image_url(event.reply_token, "https://i.imgur.com/5kxrb8z.png")
        elif event.message.text == "E2":
            send_image_url(event.reply_token, "https://i.imgur.com/mzwyyAs.png")
        elif event.message.text == "E3":
            send_image_url(event.reply_token, "https://i.imgur.com/y8gsQcX.png")
        elif event.message.text == "E4":
            send_image_url(event.reply_token, "https://i.imgur.com/JFLgmg9.png")
        elif event.message.text == "E5":
            send_image_url(event.reply_token, "https://i.imgur.com/gtzfkWI.png")
        elif event.message.text == "E6":
            send_image_url(event.reply_token, "https://i.imgur.com/07KyB0W.png")
        elif event.message.text == "返回":
            machine[user_id].go_back(event)
        elif event.message.text == "help":
            send_text_message(event.reply_token, "輸入E1~6其中一種指令取得攻略(例:E2)\n返回:回目錄")
        else:
            send_text_message(event.reply_token, "錯誤指令，如有需要請輸入help")
    elif(machine[user_id].is_information()):
        if event.message.text == "巴哈":
             send_text_message(event.reply_token, "https://forum.gamer.com.tw/A.php?bsn=24698")
        elif event.message.text == "ptt":
             send_text_message(event.reply_token, "https://www.ptt.cc/bbs/KanColle/index.html")
        elif event.message.text == "日wiki":
             send_text_message(event.reply_token, "https://wikiwiki.jp/kancolle/")
        elif event.message.text == "英wiki":
             send_text_message(event.reply_token, "https://kancolle.fandom.com/wiki/KanColle_Wiki")
        elif event.message.text == "推特":
             send_text_message(event.reply_token, "https://twitter.com/kancolle_staff")
        elif event.message.text == "返回":
            machine[user_id].go_back(event)
        elif event.message.text == "help":
            send_text_message(event.reply_token, "請輸入:巴哈,ptt,日wiki,英wiki,推特 其中一種指令取得網址\n返回:回目錄")
        else:
            send_text_message(event.reply_token, "錯誤指令，如有需要請輸入help")
    return "OK"
@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine["0"].get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)

