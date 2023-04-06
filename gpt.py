#! /usr/bin/python3
# gpt para ejecutarlo desde consola

import openai
import time
from dotenv import load_dotenv
import os
from collections import deque
cola = deque(maxlen=10)

load_dotenv()

openai_key = os.getenv("gpt_key")

openai.api_key = openai_key


while True:

    entrada = input("\n : ")
    print()

    if entrada == "exit()": 
        break
    elif entrada == "clear":
        os.system("clear")
        entrada = "hola"

    cola.append(entrada)

    # print(sum([ len(x.split()) for x in cola ]))

    while sum([ len(x.split()) for x in cola ]) > 3000:
        cola.popleft()

    conversacion = [{"role": "user", "content": x} for x in cola]


    completion = openai.ChatCompletion.create(
                    model       = "gpt-3.5-turbo",
                    messages = conversacion,

                    # messages    = [{"role": "user", "content": entrada}],
                    temperature = 1,
                    max_tokens  = 2048)
    
    cola.append(completion.choices[0].message.content)

    

    for letra in completion.choices[0].message.content:
        print(letra, end= "", flush=True)
        time.sleep(0.01)
    print()                    