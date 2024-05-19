import os
import telebot

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_API")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)


def send_notification(message):
    bot.send_message(CHAT_ID, message)
