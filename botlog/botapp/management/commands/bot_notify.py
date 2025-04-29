import telebot
from django.core.management.base import BaseCommand
from botapp.models import TelegramUserContactModel
from datetime import date as dt
from pathlib import Path
import environ
import os
from openai import OpenAI
from dataclasses import asdict
from .utils.bot_utils import START_BUTTON_MARKUP,LEAVE_ME_CONTACT_MARKUP, callback_data
from .utils.bot_utils import DEAL_BUTTONS_MARKUP,SHARE_CONTACT_MARKUP,HANDLED_MESSAGES
from .utils.bot_utils import UserMapper,store_to_redis,retrieve_from_redis
from .utils.completion_utils import completion_tools,\
                            system_instruction, update_conversations, \
                                completion_update_response,CONVERSATION_HISTORY                  
from redis import Redis


# dotenv
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# BOT - Think about: do the class with statimethods for easy usage
NOTIFY_BOT: telebot.TeleBot = telebot.TeleBot(env('BOT_NOTIFY_TOKEN'), parse_mode=None)


# redis
redis_host = env('REDIS_HOST')
redis_port = env('REDIS_PORT')
# with Redis(host=redis_host,port=redis_port) as REDIS:
#     REDIS.set(val)


# GPT Settings
client = OpenAI(
    api_key=env('OPEN_AI_KEY'),
)

        
# BUTTON CALLBACKS HANDLER
@NOTIFY_BOT.callback_query_handler(func=lambda call:True)
def callback_query(call):
    """This function handles user interaction with the InlineKeyboardButtons:
    - each button has its own callback_data
    - each callback_data are handled as match/case - pattern matching
    * show_alert = True: this param alerts -call.data- on top of the chat
    Args:
        call (CallbackQuery): telebot.types.CallbackQuery
    """
    NOTIFY_BOT.answer_callback_query(call.id,callback_data[call.data],show_alert=False)
    match call.data:
        case 'passed': 
            NOTIFY_BOT.send_message(call.message.chat.id,callback_data[call.data],reply_markup=DEAL_BUTTONS_MARKUP)
        case 'phone': 
            message_ = "Вы можете нажать - Поделиться контактом"
            NOTIFY_BOT.send_message(call.message.chat.id,message_,reply_markup=SHARE_CONTACT_MARKUP)
        case 'telegram': 
            # As an option we giving to user button 'share contact', but he may do typing too 
            message_ = "Вы можете нажать - Поделиться контактом"
            NOTIFY_BOT.send_message(call.message.chat.id,message_,reply_markup=SHARE_CONTACT_MARKUP)
        case 'later': 
            later_message = "Вы выбрали поделится позже..."
            NOTIFY_BOT.send_message(call.message.chat.id,later_message,reply_markup=DEAL_BUTTONS_MARKUP)
        case 'video': 
            # Here we need to add link or button... Need decision of people
            NOTIFY_BOT.send_message(call.message.chat.id,callback_data[call.data])
        case 'faq': 
            NOTIFY_BOT.send_message(call.message.chat.id,callback_data[call.data])
        case 'demo': 
            NOTIFY_BOT.send_message(call.message.chat.id,callback_data[call.data])
        case 'subscribe': 
            NOTIFY_BOT.send_message(call.message.chat.id,callback_data[call.data])
        case 'answer':
            # When user pushes button that have 'answer' callback_data - we do create user mapper in redis            
            current_user = UserMapper(gpt_init=True) # getting user id from call...
            store_to_redis(user_id=call.from_user.id,mapper=asdict(current_user)) # Storing to redis!
            NOTIFY_BOT.send_message(call.message.chat.id,callback_data[call.data])
        case _:
            NOTIFY_BOT.answer_callback_query(call.id,callback_data[call.data],show_alert=True)
        
        
    
# COMMANDS HANDLER
@NOTIFY_BOT.message_handler(commands=["start","help"])
def commands_handler(message):
    """This handler responds only on commands 
    * command: start  & help
    * button: 
    """
    NOTIFY_BOT.send_message(message.chat.id, env('BOT_NOTIFY_START_MESSAGE'), reply_markup=START_BUTTON_MARKUP)
 

# Contact handler
@NOTIFY_BOT.message_handler(content_types=['contact'])
def get_contact(message):
    """This method Gets TelegramContact from Message.contact
     - if message type is Contact, this contact sent to database 
    * contact: telebot.types.Contact
    """
    if message.contact:
        try:
                new_contact = TelegramUserContactModel(
                phone_number=str(message.contact.phone_number),
                first_name=str(message.contact.first_name),
                last_name= str(message.contact.last_name),
                user_id= str(message.contact.user_id),
            )
                new_contact.save()
                # If we got contact - then goes to the channel
                formated_text = env('WANTS_CONTACT_TEXT_ONE') + str(message.contact.first_name) + env('WANTS_CONTACT_TEXT_TWO') + str(message.contact.phone_number)
                NOTIFY_BOT.send_message(chat_id=env('USER_WANTS_CONTACT_CHANNEL'),text=formated_text)
                NOTIFY_BOT.reply_to(message, f"{env('USER_ADDED_TO_QUERY_CALL')}: status: OK")
        except Exception as e:
            NOTIFY_BOT.reply_to(message, f" exeption is: {str(e)}")
            
REDIS = Redis(host='localhost', port=6379, decode_responses=True)            

@NOTIFY_BOT.message_handler(func=lambda m: True)
def echoer(bot_message):
    """This handler responds on any text messages 
    while messages are not in HANDLED_MESSAGES list
    and user_data in redis temp storage has key: gpt_init = True
    * assistant : gpt-4
    """
    if retrieve_from_redis(user_id=bot_message.from_user.id): # H E R E    I S   >>>
        response = completion_update_response(
            client=client,
            messages_history=update_conversations(message=bot_message.text,conversations=CONVERSATION_HISTORY,system_instruction=system_instruction),
            completion_tools=completion_tools
            )
        if isinstance(response,list):
            # If it is list that means that is function_calling with params.
            all_call = f"{response[0]} {response[1]}"
            current_user = UserMapper(gpt_init=True) # getting user id from call...
            store_to_redis(user_id=bot_message.from_user.id,mapper=asdict(current_user))
            NOTIFY_BOT.reply_to(message=bot_message,text=all_call)
        # tex_rep = f" {response}   \n \n \n {CONVERSATION_HISTORY}"
        else:
            current_user = UserMapper(gpt_init=True) # getting user id from call...
            store_to_redis(user_id=bot_message.from_user.id,mapper=asdict(current_user))
            NOTIFY_BOT.reply_to(message=bot_message,text=response)
    else:
        return
    
    

    







class Command(BaseCommand):
    help = 'Runs Contact Notificator telegram bot with embed GPT-4  '

    def handle(self, *args, **options):
        NOTIFY_BOT.remove_webhook()
        NOTIFY_BOT.infinity_polling()



























