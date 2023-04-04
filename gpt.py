#! /usr/bin/python3
# gpt para ejecutarlo desde consola

import openai
import time
from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("gpt_key")

openai.api_key = openai_key


while True:

    entrada = input("\n : ")
    print()

    if entrada == "exit()": break

    completion = openai.ChatCompletion.create(
                    model       = "gpt-3.5-turbo", 
                    messages    = [{"role": "user", "content": entrada}],
                    temperature = 1,
                    max_tokens  = 2048)

    for letra in completion.choices[0].message.content:
        print(letra, end= "", flush=True)
        time.sleep(0.01)
    print()                    