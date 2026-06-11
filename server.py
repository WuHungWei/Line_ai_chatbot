import os
import dotenv
import json
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.getenv("CGU_OPENAI_API_KEY"),
    base_url="https://air.cgu.edu.tw/cgullmapi/v1"
)

MODEL_NAME = "gpt-5.4-mini"
MAX_HISTORY = 100

HISTORY_FILE = "chat_history.json"


def load_history():

    if not os.path.exists(HISTORY_FILE):
        return {}

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


def save_history():

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            chat_history,
            f,
            ensure_ascii=False,
            indent=4
        )


chat_history = load_history()


def add_history(user_id, role, content):

    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append({
        "role": role,
        "content": content
    })

    if len(chat_history[user_id]) > MAX_HISTORY:
        chat_history[user_id] = chat_history[user_id][-MAX_HISTORY:]

    save_history()


def clear_history(user_id):

    if user_id in chat_history:
        chat_history[user_id] = []

    save_history()


def get_history_count(user_id):

    return len(chat_history.get(user_id, []))


def ask_ai(user_id, user_message):

    history = chat_history.get(user_id, [])

    messages = [
        {
            "role": "system",
            "content": """
你是一位友善且專業的 AI 助理。

請記住目前對話內容並維持上下文一致性。
若使用者先前提過姓名、喜好、需求等資訊，
請優先根據聊天紀錄回答。

請先詢問使用者欲開發的系統功能與
需求。
AI 先協助分析需求，規劃程式架構與執行方案，並將開發流程提
供給使用者確認。
一定要等待使用者確認後，產生程式碼與開發文件。

"""
        }
    ]

    messages.extend(history)

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7
    )

    answer = response.choices[0].message.content

    add_history(user_id, "user", user_message)
    add_history(user_id, "assistant", answer)

    return answer