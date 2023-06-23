#!/home/emi/Escritorio/chatgpt/env/bin/python
# gpt para ejecutarlo desde consola
import openai
RateLimitError = openai.error.RateLimitError
InvalidRequestError = openai.error.InvalidRequestError
import time
from dotenv import load_dotenv
import os
from collections import deque
from colorama import Fore , Style 
from prompt import comandos, markdown
from PyInquirer import prompt
import webbrowser as web
import pyperclip
import signal

def handler(sig, frame):
    pass
    # print('Se ha recibido una interrupción')
    # realiza las acciones necesarias antes de finalizar el programa

signal.signal(signal.SIGINT, handler)

load_dotenv()

verde          = Fore.GREEN
azul           = Fore.BLUE 
rest           = Fore.RESET 
openai.api_key = os.getenv("gpt_key_b")
user           = os.environ["USER"]

def imagen(mensaje):

    response = openai.Image.create(
            prompt = mensaje,
            n = 1, # cantidad de imagenes puede ir de 1 a 10
            size = "1024x1024"
        )
    url = response["data"][0]["url"]
    web.open(url) # abre imagen en una pestaña
    return "Abriendo URL -> " + url

def consulta(conversacion):
    response = openai.ChatCompletion.create(
                    model       = "gpt-3.5-turbo",
                    messages    = conversacion,
                    temperature = 1,
                    max_tokens  = 2048)
    return response.choices[0].message.content , response.usage["total_tokens"]

def guardar(charla):
    if not os.path.exists("charlas"):
    # Crear la carpeta si no existe
        os.makedirs("charlas")
    archivo = input("nombre del archivo: ")
    with open("charlas/"+archivo+".txt", "w") as f:
        for line in charla:
            f.write(line+"\n")

def leer():
    archivos = os.listdir("charlas")
    opciones = [{"name": archivo} for archivo in archivos]
    respuesta = prompt({
        'type': 'list',
        'name': 'archivo',
        'message': 'Selecciona una Conversacion:',
        'choices': opciones})
    try:
        archivo = respuesta['archivo']
    except KeyError:
        return []
    with open("charlas/"+archivo, "r") as f:
        charla = f.readlines()
    return charla

def main():
    ind    = 1
    inicio = time.time()
    charla = []
    cola   = deque(maxlen=10)
    tokens = 0
    error  = False
    while True:
        if not error:
            entrada = input(f"\n{verde}{user} $: {rest}")
            if entrada.startswith("^C"): entrada = entrada[2:]
            print()
        
        if ind == 4 :
            inicio = time.time()
            ind = 0
        ind += 1

        if   entrada == "exit()": 
            break
        elif entrada == "clear":
            os.system("clear")
            #entrada = "hola"
            continue
        elif entrada == "guardar()":
            guardar(charla)
            continue
        elif entrada == "leer()":
            os.system("clear")
            charla = leer()
            if charla:
                cola = deque(maxlen=10)
                print(cola)
                for line in charla:
                    print(line.rstrip())
                    cola.append(line)
                continue
            else:
                print("Error no se pudo leer el archivo intente de nuevo sin usar el mouse")
                continue
        elif entrada == "comenta()":
            entrada = "comentame esto: \n"+ pyperclip.paste()
            print(entrada)
        elif entrada == "resumir()":
            entrada = "resumir: \n"+ pyperclip.paste()
            print(entrada)
        elif entrada == "pegar()":
            entrada = pyperclip.paste()
            print(entrada)
        elif entrada == "nueva()":
            os.system("clear")
            charla = []
            cola   = deque(maxlen=10)
            continue
        elif entrada == "traducir()" or entrada == "tr":
            entrada = "traducir al español :\n" + pyperclip.paste()    
        elif entrada == "markdownd()" or entrada == "mark()":
            entrada =  markdown + pyperclip.paste()  
        elif (im_promt := entrada.split(" ", maxsplit=1))[0] == "/imagen":
            prt = consulta ( [{"role": "user","content": "traducir al el ingles: " + im_promt[1]}])
            print(imagen(prt))
            continue                     
        elif (com := entrada.lower()[:3]) in comandos:
            entrada = comandos[com] + entrada
        
        if not error:
            charla.append(user+" :"+ entrada)
            cola.append(entrada)

        conversacion = [{"role": "user", "content": x} for x in cola]
    
        try:
            respuesta , tokens = consulta(conversacion)
        except RateLimitError as e:
            print(e)
            texto = "Error, solo 3 mensjes por minuto restan :"
            times = 60 - (int(time.time() - int(inicio)))
            for i in range(times):
                print (texto + str(times - i).zfill(2), end= "\b" * (len(texto)+2), flush=True)
                time.sleep(1)
            error = True           
        except InvalidRequestError:
            print("Se superaron los tokens")
            # print("total de tokens :", tokens)
            
            if input("reducimos contexto S/N? o reduci la cantidad de palabras del promtp :").lower() == "s":
                error = True
                try:
                    cola.popleft()
                except IndexError:
                    print("el contexto esta vacio, reduzca el prompt")
                    error = False
                    continue
                else:
                    time.sleep(1)
            else:
                error = False
                continue
            
        # except Exception as e:
        #     print("ERROR :" + str(type(e)) + str(e))
        #     error = True
        #     cola.popleft()
        #     time.sleep(1)
        else:
            error = False
            cola.append(respuesta)
            charla.append("GPT $:"+ respuesta) 
            print(f"{azul}GPT $: {rest}", end="")
            for letra in respuesta:
                print(letra, end= "", flush=True)
                time.sleep(0.01)
            print()                    

if __name__ == "__main__":
    main()