import json
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
from .models import UserContactModel
from starlette import status
from .management.commands.bot_notify import NOTIFY_BOT
import environ
import os



# dotenv
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# HELLO INDEX VIEW
def index(request):
    addition_text = '<br>BP - Marketing Bot</br>' + '<br> Status OK </br>'
    return HttpResponse(addition_text)
    



@csrf_exempt
@api_view(['GET'])
def send_user_query_data(request):
    """This method gets user data from url query params, 
    - then puts these in a database
     - Then second option is that this method sends data about the user to the telegram bot
     - bot alerts that the user from query params wants to have phone conversation...
    - query params: request
        * name
        * email
        * phone
        * comment
        * contact
    """
    name = request.GET.get('name')
    email = request.GET.get('email')
    phone = request.GET.get('phone')
    comment = request.GET.get('comment')
    contact = request.GET.get('contact')
    # contact_obj
    if not phone or not email:
        return  JsonResponse({'status': status.HTTP_400_BAD_REQUEST, 'message': 'bad request'})
    try:
        new_user = UserContactModel(name=name,email=email,phone=phone,comment=comment,contact=contact)
        new_user.save()
        formated_text = env('WANTS_CONTACT_TEXT_ONE') + name + env('WANTS_CONTACT_TEXT_TWO') + phone + " " + contact
        NOTIFY_BOT.send_message(chat_id=env('USER_WANTS_CONTACT_CHANNEL'),text=formated_text)
        return JsonResponse({'status': status.HTTP_201_CREATED, 'message': 'created'})
    # If server error exception goes to the message
    except Exception as e:
        return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})



# @csrf_exempt
# @api_view(['POST'])
# def post_user_data(request):
#     """The POST handler that receives UserContactModel who have sent data on website user form 
#     Comment: 
#     - query params: request
#         * name
#         * email
#         * phone
#         * comment
#         * contact
#     """
#     if request.method == 'POST':
#         dict_request = request.data #json.loads(stringify_data) # making dict for convenience 
#         try:
#             new_user = UserContactModel(name=dict_request['name'],email=dict_request['email'],phone=dict_request['phone'],comment=dict_request['comment'],contact=dict_request['contact'])
#             new_user.save()
#             formated_text = env('WANTS_CONTACT_TEXT_ONE') + dict_request['name'] + env('WANTS_CONTACT_TEXT_TWO') + dict_request['phone'] + " " + dict_request['contact']
#             NOTIFY_BOT.send_message(chat_id=env('USER_WANTS_CONTACT_CHANNEL'),text=formated_text)
#             return JsonResponse({'status': status.HTTP_201_CREATED, 'message': 'created'})
#     # If server error exception goes to the message
#         except Exception as e:
#             return JsonResponse({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e)})
#     else:
#         return JsonResponse({'status':status.HTTP_405_METHOD_NOT_ALLOWED,'message':'not allowed'})



