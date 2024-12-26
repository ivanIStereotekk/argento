from django.urls import path
from .views import send_user_query_data,index




urlpatterns = [
     path('send_user_query_data/', send_user_query_data, name='send_user_query_data'),
     # path('post_user_data/',post_user_data,name='post_user_data'),
     path('',index,name='index')    
]