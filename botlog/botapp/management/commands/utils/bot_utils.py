import telebot
import environ
from pathlib import Path
from telebot.types import KeyboardButton,ReplyKeyboardMarkup
from telebot.util import quick_markup
import os
import redis
from redis import Redis
import json
from dataclasses import dataclass, field, asdict
from tiktoken import encoding_for_model
# redis
REDIS = redis.Redis(host='localhost',port=6379)

# env
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Telegram Bot interaction messages:

start_message = env('BOT_NOTIFY_START_MESSAGE')

leave_me_contact_message = env('BOT_NOTIFY_LEAVE_ME_CONTACT')

# Dict with callback_data and alerts that will appear on top of chat
callback_data = dict(
       passed='Вы пропустили...',
       phone='Берем номер...',
       telegram='Получаем конт...',
       later='Позже...',
       video='Высылаем видеофайл...',
       demo='Готовим демо-версию...',
       answer='Запускаем ассистента...',
       faq='Frequently Asked Questions...',
       subscribe='Подписаться...',    
       )

HANDLED_MESSAGES = ['start', 'help','contact'] 

#  [i for i in callback_data.keys()]

# markups:
START_BUTTON_MARKUP = quick_markup({'💁‍♂️ Пропустить': {'callback_data': 'passed'}},row_width=1)
# leave me buttons
LEAVE_ME_CONTACT_MARKUP = quick_markup(
                                        {'☎ Номер телефона':{'callback_data':'phone'},
                                        '📲 Telegram':{'callback_data':'telegram'},
                                        'Поделиться позже': {'callback_data':'later'}
                                        },row_width=2
                                        )

DEAL_BUTTONS_MARKUP = quick_markup(
       {'💡 Показать видеоинструкцию по BusinessPad':{'callback_data':'video'},
        '📦 Дать доступ к демо-версии':{'callback_data':'demo'},
        '❓ Ответить на вопросы': {'callback_data':'answer'},
        '📚 Показать FAQ':{'callback_data':'faq'},
        '📢 Также Вы можете подписаться на наши соцсети, чтобы постоянно быть в курсе новостей про IT и про бизнес':{'callback_data':'subscribe'}
       },row_width=1
)

# CONTACT SHARING 
SHARE_CONTACT_MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
SHARE_CONTACT_MARKUP.add(KeyboardButton(text="Поделиться своим контактом.",request_contact=True))


# GPT settings

# tokenizer
encoding = encoding_for_model("gpt-4o-mini")

def num_tokens_from_string(string):
    """Returns count of tokens"""
    return len(encoding.encode(string))



# REDIS ACTIONS

def store_to_redis(chat_id: str, mapper: dict):
    """Storing data to Redis storage
    Args:
        chat_id (str): message.chat.id
        mapper (dict): asdict( UserMapper() )
    """
    value = json.dumps(mapper)
    conn = redis.Redis(host='localhost', port=6379)
    conn.set(chat_id,value)
    conn.expire('key1',time=600)


def retrieve_from_redis(chat_id):
    """Retrieve item from Redis 
    Args:
        chat_id (_type_): is a key
    Returns:
        _type_: python dict
    """
    conn = redis.Redis(host='localhost', port=6379, decode_responses=True)
    result = conn.get(chat_id)
    return json.loads(result)
        
    

@dataclass 
class UserMapper:
    """Temp storage item for Redis
    * key is - Message.chat.id
    * typed_name - name that typed user while asked name
    * typed telegram @username
    * gpt_init - key that shows in GPT conversation thread 
    """
    typed_name: str = field(default=None)
    typed_username: str = field(default=None)
    gpt_init: bool = field(default=False)

    
@dataclass
class MessageMapper:
    role: str = field(default=None)
    content: str = field(default=None)



    
    
   

    
    
    
