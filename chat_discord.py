import discord 
from dotenv import load_dotenv
import os
import openai
from collections import deque
from prompt import prompt_bienvenida , comandos

load_dotenv()

discord_token  = os.getenv("bot_key")
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


class MyClient(discord.Client):

    async def on_ready(self):
        print ("Client ready")
               
    async def on_message(self,message):
        print (message.author)
        print (message.content)
        print (message.channel)
        if not str.startswith(str(message.channel),"Direct"): 
            # print (message.channel.category)
            us = (str(message.channel.category),str(message.channel))
        else:
            us = str(message.author)

        if message.author == self.user:
            return
        elif message.content == "":
            await message.channel.send(gpt(us,prompt_bienvenida.format(str(message.author)[:-5])))
            return
        elif message.content.lower() in ["help","ayuda","/?","?"]:
            st = ""
            for key, value in list(comandos.items())[3:]:
                print(key,value)
                st += "para "+value+key+"\n"
            await message.channel.send(f"Bienvenido {str(message.author)[:-5]}\npara usar gpt : /bot \n" + st) 
            return
        else:
            command , user_message = None, None

        for text in list(comandos.keys()) + ["/img"]:
            if message.content.startswith(text):
                command = message.content.split(" ")[0]
                user_message = message.content.replace(text,"")
                print("commando :",command, "\nmensaje :",user_message)

        if command is None or command not in comandos:
            return

        elif command.lower() == "/chat":
            res = chat(user_message)
            await message.channel.send(f"chat : {res}")
        elif command.lower() == "/img":
            print("pidiendo image :",user_message)

            url = imagen(user_message)
            await message.channel.send(url)
            return

        else:
            user_message = comandos[command] + user_message 

        try:
            res = gpt(us,user_message)
        except Exception as e:
            await message.channel.send("### Error del servidor, por favor repita la consulta ###")          
        else:
            if len(res) > 2000:
                chunked_messages = [res[i:i+1500] for i in range(0, len(res), 1500)]
                await message.channel.send("chat : La Respuesta exede los caracteres permitidos para discord \nesta  fraccionada en mensajes de 1500 caracteres")
                for parte , chunk in enumerate (chunked_messages,1):
                    await message.channel.send(f"chat {str(parte)}/{len(chunked_messages)}: {chunk}")
            else:
                await message.channel.send(f"chat : {res}")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(discord_token)