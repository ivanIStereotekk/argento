from rest_framework import serializers
from .models import UserContactModel,TelegramBotDialogModel,TelegramUserContactModel
# from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserContactSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for UserContactModel

    Args:
        serializers (_type_): json serializer
    """
    class Meta:
        model = UserContactModel
        fields = ['name', 'phone', 'email', 'comment','contact']


class TelegramUserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TelegramUserModel

    Args:
        serializers (_type_): json serializer
    """
    class Meta:
        model = TelegramUserContactModel
        fields = ['telegram_id', 'firstname', 'lastname', 'username','phone']


class TelegramMessageSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for TelegramBotDialogModel

    Args:
        serializers (_type_): json serializer
    """
    class Meta:
        model = TelegramBotDialogModel
        fields = ['username', 'prompt','created','response']


