from django.db import models
from django.core.validators import RegexValidator






class UserContactModel(models.Model):
    """User Contact That comes from GET url query params from the http request
    * name: str
    * email: str [ email field] 
    * comment: str 
    * created: datetime.date (auto add now)
    * phone: str[ numeric ]
    """
    name = models.CharField(max_length=77,verbose_name="Имя")
    email = models.EmailField(verbose_name="Электронная почта")
    comment = models.TextField(verbose_name="Комментарий")
    created = models.DateField(auto_now=True,verbose_name="Дата создания")
    phone = models.CharField(
        max_length=20, 
        verbose_name="Телефон",
        # validators=[
        #     RegexValidator(
        #         regex=r'^\+?1?\d{9,15}$',  
        #         message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        #     )
        # ]
    )
    contact =models.TextField(max_length=255,default="#",verbose_name="Контакт")
    class Meta:
        verbose_name = 'Контакт с формы на сайте'
        verbose_name_plural = 'Контакты с формы на сайте'
    def __str__(self):
        return f"Name: {self.name}   Created: {self.created}"
    
    
    

class TelegramUserContactModel(models.Model):
    """Telegram User That Initiated Interaction With The Bot
    - When user leaves his contact that contact saved as TelegramUserContactModel
    * user_id: int
    * first_name: str 
    * last_name: str 
    * created: datetime.date 
    * phone_number: str[ numeric ]
    
    """
    user_id = models.IntegerField(verbose_name="Идентификатор в телеграм") # id
    first_name = models.CharField(max_length=35,verbose_name="Имя")
    last_name = models.CharField(max_length=35,verbose_name="Фамилия")
    created = models.DateField(auto_now=True,verbose_name="Дата создания")
    phone_number = models.CharField(
        verbose_name="Телефон",
        max_length=20,
        # validators=[
        #     RegexValidator(
        #         regex=r'^\+?1?\d{9,15}$',
        #         message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        #     )
        # ]
    )
    def __str__(self):
        return f"First-name: {self.first_name}   Created: {self.created}"
    class Meta:
        verbose_name = 'Контакт из Телеграмм'
        verbose_name_plural = 'Контакты из Телеграмм'

class TelegramBotDialogModel(models.Model):
    """Chat Message or Prompt Initiated by user into Telegram GPT-4 Chat
    * username: str
    * prompt: str
    * response: str
    * created: datetime.date
    """
    username = models.CharField(max_length=35,verbose_name="Имя пользователя")
    prompt = models.TextField(verbose_name="Вопрос к ассистенту")
    response = models.TextField(verbose_name="Ответ от ассистента")
    created = models.DateField(auto_now=True,verbose_name="Дата сообщения")
    def __str__(self):
        return f"Username: {self.username}   Created: {self.created}"
    class Meta:
        verbose_name = "Запись диалога с ботом"
        verbose_name_plural = "Записи диалогов с ботом"


            
