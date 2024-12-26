from openai import OpenAI

import json




system_instruction = """
Вы ассистент а зовут вас Надежда. Вы работаете в компании BusinessPad, продвигаете программные продукты компании, 
рассказываете людям о их приемуществах и возможностях. Ваша IT-компания предлагает качественные решения для бизнеса, 
руководителей и IT — компаний. За 19 лет работы на рынке технологий вы накопили уникальный опыт разработки, 
внедрения и сопровождения комплексных систем автоматизации бизнес-процессов.
Эффективная и сплоченная команда успешно реализует поставленные задачи.
Внедрение системы управления ресурсами Business Pad обеспечивает своевременное выполнение задач, 
улучшает коммуникацию между отделами и способствует достижению стратегических целей организации.
BusinessPad это, CRM и ERP — инструменты, продвинутый конструктор процессов предназначенный для выполнения разных задач.
Основные возможности:
Моделирование бизнес-процессов
События, шлюзы и циклы
Процессы, задачи и потоки операций
Секции и зоны ответственности
Представление правил и переменных
---
Детальный учет финансов
Управление денежными потоками
Прогнозирование прибыли
Неограниченное число объектов учёта
Бюджетирование
Мультивалютность
Отчёты БДР и БДДС
---
Мобильное приложение
Работа в любом месте и в любое время
Быстрый доступ к данным
Возможность оперативно принимать решения
Уведомления о событиях, задачах и действиях по процессам
Процессы в BP — это схемы бизнес-процессов компании. 
По ним создаются конкретные —
сущности:
сделки;
отчёты;
HR-процессы;
алгоритмы производства товаров с описанием производственных линий;
финансовые процессы;
отгрузка товаров;
логистика;
документооборот и т. д.
---
Ваша основная задача:
Рассказать собеседнику о пользе предлагаемого продукта.
Собрать контактные данные пользователя для того чтобы в последствии выслать ему демонстрационный пакет услуг.
Вы должны получить у пользователя его email, его никнейм в мессенджере телеграм, очень важно получить телефонный номер.
Не стесняйтесь просить номер несколько раз, рассказывайте о приемуществах в случае если вы ему вышлите демонстрационный пакет ПО.
---
Если ваш собеседник вводит в сообщении свои контакты, и в этих данных контактов набор хотябы из [ email, phone ] или [telegram_id, phone ] то вы должны запустить "collect_user_contacts" tool и в качестве аргуметнов взять введеные собеседником контакты.
Если собеседник просит прислать ему кнопки то вы должны спросить какой тип кнопок ему нужен (по материалам БизнесПэд, или поделиться своим контактом), а затем запускаете фунцию "send_keyboard_buttons" tool.
Если ваш собеседник просит выслать дэмо материал вы должны запустить, "send_demo_package_to_user" tool.
Если вам сказали всего доброго, вы должны ответить - рада сотрудничеству! Всего вам наилучшего !


"""



# tools or function calls

completion_tools = [
    {
      "type": "function",
      "function": {
          "name": "collect_user_contacts",
          "description": "Collecting users contacts information, collecting info then saving it in the database for future business needs",
          "parameters": {
              "type": "object",
              "properties": {
                  "name": {"type": "string"},
                  "surname": {"type": "string"},
                  "phone": {"type": "string"},
                  "email": {"type": "string"},
                  "telegram_id": {"type":"string" },
                  },
              },},},
    {
      "type": "function",
      "function": {
          "name": "send_demo_package_to_user",
          "description": "This function makes sending demo package or documents to user contact it depends of the given contact or address also it's important to know what kind of content",
          "parameters": {
              "type": "object",
              "properties": {
                  "address": {"type": "string"},
                  "content": {"type": "string"},
                  },
              },},},
    {
      "type": "function",
      "function": {
          "name": "send_keyboard_buttons",
          "description": "Sending buttons & keyboards in conversation thread for interaction with the system/chat by pushing buttons. When guest asks to send buttons to him you should call - 'send_keyboard_buttons' - function, with argument 'action_type' ",
          "parameters": {
              "type": "object",
              "properties": {
                  "action_type": {"type": "string"},
                  },
              },},},
]
    
CONVERSATION_HISTORY = []


def update_conversations(
    message: str = None,
    response: str = None,
    conversations: list = [],
    system_instruction: str = None
    ):   
    """ Updates Conversation list: massage_history
    - users message - message
    - or bots response - response
    Args:
        message (_type_, optional): _description_. Defaults to None.
        response (_type_, optional): _description_. Defaults to None.
        conversations (list, optional): _description_. Defaults to [].

    Returns:
        _type_: list of messages
    """
    system_message = {"role":"system","content": system_instruction}
    if system_message not in conversations and system_instruction is not None:
        conversations.append(system_message)
    if message is not None:
        new_user_message = {"role": "user", "content": message}
        conversations.append(new_user_message)
    if response is not None:
        new_response = {"role":"assistant", "content": response }
        conversations.append(new_response)
    return conversations
    

    
def completion_update_response(client:OpenAI,messages_history:list,completion_tools:list) -> str:
    """Complation OpenAI response maker
        and function caller
    Args:
        client (OpenAI): _description_
        messages_history (list): list of messages
        complation_tools (list): function calls that shoul be called
    Returns:
        str: text message
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=messages_history,
            tools=completion_tools,
        )
        if completion.choices[0].message.tool_calls:
            tool_call = completion.choices[0].message.tool_calls 
            tool_function = tool_call[0].function
            tool_function_name = tool_function.name
            tool_function_type = tool_call[0].type
            arguments = tool_function.arguments
            dicted_args = json.loads(arguments)
            # THis place for pushin user data to database
            return  [ tool_function_name, arguments ]        #completion.choices[0].message.tool_calls 
        if completion.choices[0].message.content:
            return completion.choices[0].message.content
    except Exception as e:
        return f"Response: 404   details: {e} "