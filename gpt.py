#! /usr/bin/python3
# gpt para ejecutarlo desde consola
import openai
RateLimitError = openai.error.RateLimitError
import time
from dotenv import load_dotenv
import os
from collections import deque
from colorama import Fore , Style 
import pickle

load_dotenv()

verde          = Fore.GREEN
azul           = Fore.BLUE 
rest           = Fore.RESET 
cola           = deque(maxlen=10)

openai.api_key = os.getenv("gpt_key")
user           = os.environ["USER"]

def consulta(conversacion):
    return openai.ChatCompletion.create(
                    model       = "gpt-3.5-turbo",
                    messages = conversacion,
                    temperature = 1,
                    max_tokens  = 2048).choices[0].message.content

ind = 0
inicio = time.time()
while True:

    entrada = input(f"\n{verde}{user} $: {rest}")
    print()
    if ind == 3 :
        inicio = time.time()
        ind = 0
    ind += 1

    if entrada == "exit()": 
        break
    elif entrada == "clear":
        os.system("clear")
        entrada = "hola"
    elif entrada.lower().startswith("/es"):
        entrada = "traducir al español :" + entrada
    elif entrada.lower().startswith("/en"):
        entrada = "traducir al ingles :" + entrada

    cola.append(entrada)
    tokens = sum([ len(x.split()) for x in cola ])

    while  (tokens := sum([ len(x.split()) for x in cola ])) > 3000:
        cola.popleft()


    conversacion = [{"role": "user", "content": x} for x in cola]

    try:
        respuesta = consulta(conversacion)

    except RateLimitError:
        print ("Error")
        time.sleep (int(time.time() - inicio))
    
    except Exception as e:
        print("ERROR :" + str(e))
        time.sleep(2)
        continue
    else:
        cola.append(respuesta)
    
        print(f"{azul}GPT $: {rest}", end="")
    
        for letra in respuesta:
            print(letra, end= "", flush=True)
            time.sleep(0.01)
        print()                    
