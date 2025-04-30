import telebot
from django.core.management.base import BaseCommand
from botapp.models import TelegramUserContactModel
from datetime import date as dt
from pathlib import Path
import environ
import os
from dataclasses import asdict            
from redis import Redis


# dotenv
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# оставил только Телеграм бота
# BOT - Think about: do the class with statimethods for easy usage
NOTIFY_BOT: telebot.TeleBot = telebot.TeleBot(env('BOT_NOTIFY_TOKEN'), parse_mode=None)


# redis
redis_host = env('REDIS_HOST')
redis_port = env('REDIS_PORT')




# !!! Создать класс builder для того чтобы на каждую тему отвечал свой ассистент

# assistant working example
@NOTIFY_BOT.message_handler(func=lambda m: True)
def echoer(bot_message):
    """This handler responds on any text messages 
    while messages are not in HANDLED_MESSAGES list
    * assistant : gpt-4
    """
    formated = "NONE NONE"
    NOTIFY_BOT.send_message(chat_id=bot_message.chat.id,text=formated)

    
        
        
        
class Command(BaseCommand):
    help = 'Runs Contact GPT-4 assistant on telegram Bot Base  '

    def handle(self, *args, **options):
        NOTIFY_BOT.remove_webhook()
        NOTIFY_BOT.infinity_polling()