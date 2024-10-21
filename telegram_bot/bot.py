from telebot.async_telebot import AsyncTeleBot
import os
from dotenv import load_dotenv


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT')
bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN, parse_mode='HTML')


@bot.message_handler(commands=['help', 'start'])
async def start(message):
    ### Return errors from main functions
    text = ('')
    await bot.reply_to(message, text)







