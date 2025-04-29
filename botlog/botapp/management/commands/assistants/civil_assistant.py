from openai import OpenAI
from pathlib import Path
import environ
import os
from redis import Redis


# dotenv
env = environ.Env(DEBUG=(bool,False))
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))




# redis
redis_host = env('REDIS_HOST')
redis_port = env('REDIS_PORT')


client = OpenAI(
    api_key=env('OPEN_AI_KEY'),
)


system_instruction = """
Вы юрист консультант по гражданскому праву. Вы помогаете разобраться в имущественных спорах, оказываете помощь
в правовых конфликтах, гражданских судебных делах, даете консультации по формированию правильной правовой позиции, 
помогаете людям узнавать о своих правах в спорах связаннх с гражданским кодексом.
- Вы даете консультации только по гражданскому праву.
- Вы даете консультации не длиннее 600 слов.
- При каждом удобном случае вы цитируете гражданский кодекс РФ.
"""













# assistant
assistant = client.beta.assistants.create(
    model="gpt-4o",
    name="Консультант по гражданским правам",
    instructions=system_instruction,
    tools=[{"type": "file_search"}],
    )

# vector store
vector_store = client.beta.vector_stores.create(name="Civil Code")
file_paths = ["/Users/ewan/Desktop/Dev/bot-station/codes-pdf/Civil-Code-Addition-Ru.pdf","/Users/ewan/Desktop/Dev/bot-station/codes-pdf/Civil-Code-Ru.pdf"]
# file streams
file_streams = [open(path,'+rb') for path in file_paths]
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(vector_store_id=vector_store.id,files=file_streams)
print(file_batch.status,"<<< STATUS")
print(file_batch.file_counts,"  : COUNTS")
assistant = client.beta.assistants.update(assistant_id=assistant.id)