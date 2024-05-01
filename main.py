import traceback
import telebot
from telebot import types
from api import Api
import config
from dtos import CreateUser


TOKEN = config.TOKEN

bot = telebot.TeleBot(TOKEN, threaded=False)

api = Api(config.SERVER_URL)


@bot.message_handler(commands=["start"], chat_types=["private"])
def start(message: types.Message):
    chat_id = user_id = message.from_user.id

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            "Open web app",
            web_app=types.WebAppInfo(url=config.SITE_URL),
        )
    )

    user_photos = bot.get_user_profile_photos(user_id, limit=1)

    if user_photos.photos:
        file_id = user_photos.photos[0][0].file_id
        file_url = bot.get_file_url(file_id)
    else:
        file_url = ''

    api.register_user(
        CreateUser(
            user_id=user_id,
            username=message.from_user.username,
            fullname=message.from_user.full_name,
            photo_url=file_url,
        )
    )
    bot.send_message(
        chat_id,
        "Hello in bot",
        reply_markup=keyboard,
    )


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        with open("logs.txt", "a", encoding="utf-8") as f:
            f.write(f"{traceback.format_exc()}\n")
        print(e)
"""         try:
            bot.send_message(-1001999436200, traceback.format_exc())
        except:
            pass """
