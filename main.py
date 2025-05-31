from flask import Flask, request, jsonify
import traceback
import telebot
from telebot import types
import requests
from api import Api
import config
from dtos import CreateUser

TOKEN = config.TOKEN
bot = telebot.TeleBot(TOKEN, threaded=False)
api = Api(config.SERVER_URL)

TELEGRAM_API_URL = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)

app = Flask(__name__)


def send_telegram_message(user_id: int, text: str):
    try:
        response = requests.post(
            TELEGRAM_API_URL,
            json={"chat_id": user_id, "text": text},
            timeout=5
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"Error sending Telegram message via HTTPS: {e}\n")
        return False


@app.route("/send_message", methods=["POST"])
def api_send_message():
    try:
        data = request.json
        user_id = data.get("user_id")
        text = data.get("text")

        if not user_id or not text:
            return jsonify({"error": "Missing 'user_id' or 'text' field."}), 400

        success = send_telegram_message(user_id, text)

        if success:
            return jsonify({"status": "Message sent"})
        else:
            return jsonify({"error": "Failed to send message"}), 500

    except Exception as e:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{traceback.format_exc()}\n")
        return jsonify({"error": "Internal server error"}), 500


@bot.message_handler(commands=["start"], chat_types=["private"])
def start(message: types.Message):
    chat_id = user_id = message.from_user.id

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "Launch Splitty",
            web_app=types.WebAppInfo(url=config.SITE_URL),
        )
    )
    user_photos = bot.get_user_profile_photos(user_id, limit=1)

    if user_photos.photos:
        file_id = user_photos.photos[0][0].file_id
        file_url = bot.get_file_url(file_id)
    else:
        file_url = ''

    parts = message.text.split()
    code = parts[1] if len(parts) > 1 else None

    api.register_user(
        CreateUser(
            user_id=user_id,
            username=message.from_user.username,
            fullname=message.from_user.full_name,
            photo_url=file_url,
            referred_by_code=code,
        )
    )
    bot.send_message(
        chat_id,
        "Welcome to Splitty",
        reply_markup=keyboard,
    )


if __name__ == "__main__":
    from threading import Thread

    def start_polling():
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                with open("logs.txt", "a", encoding="utf-8") as f:
                    f.write(f"{traceback.format_exc()}\n")
                print(e)
                try:
                    send_telegram_message(254960854, traceback.format_exc())
                except:
                    pass

    Thread(target=start_polling).start()
    app.run(host="0.0.0.0", port=5000)