import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

machine = TocMachine(
    states=["user", "music", "exam", "first", "first_1", "first_2", 
            "second", "second_1", "second_2", 
            "third", "third_1"],
    transitions=[
        {#goto 音樂 
            "trigger": "advance",
            "source": "user",
            "dest": "music",
            "conditions": "is_going_to_music",
        },
        {#goto 考古
            "trigger": "advance",
            "source": ["user", "music"],
            "dest": "exam",
            "conditions": "is_going_to_exam",
        },
        {#考古->大一
            "trigger": "advance",
            "source": "exam",
            "dest": "first",
            "conditions": "is_going_to_first",
        },
        {#大一->大一上
            "trigger": "advance",
            "source":"first",
            "dest": "first_1",
            "conditions": "is_going_to_first_1",
        },
        {#大一->大一下
            "trigger": "advance",
            "source":"first",
            "dest": "first_2",
            "conditions": "is_going_to_first_2",
        },
        {#考古->大二
            "trigger": "advance",
            "source": "exam",
            "dest": "second",
            "conditions": "is_going_to_second",
        },
        {#大二->大二上
            "trigger": "advance",
            "source":"second",
            "dest": "second_1",
            "conditions": "is_going_to_second_1",
        },
        {#大二->大二下
            "trigger": "advance",
            "source":"second",
            "dest": "second_2",
            "conditions": "is_going_to_second_2",
        },
        {#考古->大三
            "trigger": "advance",
            "source": "exam",
            "dest": "third",
            "conditions": "is_going_to_third",
        },
        {#大三->大三上
            "trigger": "advance",
            "source":"third",
            "dest": "third_1",
            "conditions": "is_going_to_third_1",
        },
        {#每次找完都會回到科目選擇狀態
            "trigger": "advance",
            "source":"first_1",
            "dest": "first",
            "conditions": "on_enter_first_1",
        },
        {#每次找完都會回到科目選擇狀態
            "trigger": "advance",
            "source":"first_2",
            "dest": "first",
            "conditions": "on_enter_first_2",
        },
        {#每次找完都會回到科目選擇狀態
            "trigger": "advance",
            "source":"second_1",
            "dest": "second",
            "conditions": "on_enter_second_1",
        },
        {#每次找完都會回到科目選擇狀態
            "trigger": "advance",
            "source":"second_2",
            "dest": "second",
            "conditions": "on_enter_second_2",
        },
        {#每次找完都會回到科目選擇狀態
            "trigger": "advance",
            "source":"third_1",
            "dest": "third",
            "conditions": "on_enter_third_1",
        },
        {#回到初始狀態
            "trigger": "advance",
            "source": ["music", "exam", "first", "first_1", "first_2", 
                        "second", "second_1", "second_2", 
                        "third", "third_1"], 
            "dest": "user",
            "conditions": "is_going_to_bye",
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


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


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
