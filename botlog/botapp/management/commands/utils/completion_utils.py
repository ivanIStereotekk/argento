from openai import OpenAI

import json




system_instruction = """
Вы юрист консультант по гражданскому праву. Вы помогаете разобраться в имущественных спорах, оказываете помощь
в правовых конфликтах, гражданских судебных делах, даете консультации по формированию правильной правовой позиции, 
помогаете людям узнавать о своих правах в спорах связаннх с гражданским кодексом.
- Вы даете консультации только по гражданскому праву.
- Вы даете консультации не длиннее 600 слов.
- При каждом удобном случае вы цитируете гражданский кодекс РФ.
"""


# system_instruction = """
# Вы врач психиатр. Вы помогаете людям в сложных ситуациях.
# Вашей основной деятельностью как врача является профилактика, диагностика и лечение психических расстройств.
# - Вы даете консультации только по психиатрии.
# - Вы даете консультации не длиннее 800 слов.
# - При каждом удобном случае вы цитируете литературу которая у вас есть в vector_store.
# """





file_search_tool = [{"type":"file_search"}]


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
    
# CODES PDF    
file_paths = ["/Users/ewan/Desktop/Dev/bot-station/codes-pdf/Civil-Code-Addition-Ru.pdf","/Users/ewan/Desktop/Dev/bot-station/codes-pdf/Civil-Code-Ru.pdf"]


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
    





def update_assistant_conversations(
    message: str = None,
    response: str = None,
    conversations: list = [],
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

    if message is not None:
        new_user_message = {"role": "user", "content": message}
        conversations.append(new_user_message)
    if response is not None:
        new_response = {"role":"assistant", "content": response }
        conversations.append(new_response)
    return conversations







    
def completion_update_response(client:OpenAI,messages_history:list,completion_tools:list) -> str:
    """Completion OpenAI response maker
        and function caller
    Args:
        client (OpenAI): _description_
        messages_history (list): list of messages
        completion_tools (list): function calls that shoul be called
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
    
    
    
def vector_store_and_batch_builder(client: OpenAI,file_paths: list):
    """This function creates vector store object

    Args:
        client (OpenAI): _description_
        file_paths (list): _description_
    Returns:
        _type_: vector_store 
        _type_: file_butch
    """
    try:
        vector_store = client.beta.vector_stores.create(name="Psychiatrists handbook")
        file_paths = ["/Users/ewan/Desktop/Dev/bot-station/psychiatrist/Kaplan_Clinical_Psychiatry.pdf","/Users/ewan/Desktop/Dev/bot-station/psychiatrist/Oxford_Handbook.pdf"]
        
        
        # vector_store = client.beta.vector_stores.create(name="Civil Code")
        # file_paths = ["/Users/ewan/Desktop/Dev/bot-station/codes-pdf/Civil-Code-Addition-Ru.pdf","/Users/ewan/Desktop/Dev/bot-station/codes-pdf/Civil-Code-Ru.pdf"]
        file_streams = [open(path,'+rb') for path in file_paths]
        file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,files=file_streams
                                                            )
        return vector_store,file_batch
    except Exception as e:
        return f"error:{e}"

    
    
    file_paths_psychiatric = ["/Users/ewan/Desktop/Dev/bot-station/psychiatrist/Kaplan_Clinical_Psychiatry.pdf"]