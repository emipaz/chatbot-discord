import openai
import os
from collections import deque
from dotenv import load_dotenv

load_dotenv()

openai_key     = os.getenv("gpt_key")
openai.api_key = openai_key

chats = dict()

def leer(us):
    chats[us] = chats.get(us, deque(maxlen=10))
    return chats
    
def gpt(us, entrada):
    
    chats = leer(us)
    chats[us].append(entrada)

    while (tokens := sum ( [len(x.split()) for x in chats[us]])) > 2048:
        chats[us].popleft()
    
    # print(len(chats[us]), tokens)

    prompt = [{"role": "user", "content": x} for x in chats[us]]

    completion = openai.ChatCompletion.create(
                    model       = "gpt-3.5-turbo", 
                    messages    = prompt,
                    temperature = 1,
                    max_tokens  = 2048)
    chats[us].append(completion.choices[0].message.content)
    # print(chats)
    return completion.choices[0].message.content

def chat (entrada):
    completion = openai.Completion.create(
        engine ="text-davinci-003",
        prompt = entrada,
        max_tokens = 2048)
    return completion.choices[0].text

def imagen(mensaje):
    print(mensaje)

    response = openai.Image.create(
            prompt = mensaje,
            n = 1, # cantidad de imagenes puede ir de 1 a 10
            size = "1024x1024"
        )
    # print(response)
    url = response["data"][0]["url"]
    return  url
