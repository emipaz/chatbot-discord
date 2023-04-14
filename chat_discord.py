import discord 
from dotenv import load_dotenv
import os
import openai
from collections import deque

load_dotenv()

discord_token  = (os.getenv("bot_key"))
openai_key     = os.getenv("gpt_key")

openai.api_key = openai_key

contexto = deque(maxlen=10)


def gpt(entrada):
    contexto.append(entrada)

    
    while (tokens := sum ( [len(x.split()) for x in contexto])) > 2048:
        contexto.popleft()
    print(len(contexto), tokens)

    prompt = [{"role": "user", "content": x} for x in contexto]

    completion = openai.ChatCompletion.create(
                    model       = "gpt-3.5-turbo", 
                    messages    = prompt,
                    temperature = 1,
                    max_tokens  = 2048)
    contexto.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

def chat (entrada):
    completion = openai.Completion.create(
        engine ="text-davinci-003",
        prompt = entrada,
        max_tokens = 2048)
    return completion.choices[0].text


class MyClient(discord.Client):

    async def on_ready(self):
        print ("Client ready")
               
    async def on_message(self,message):
        print (message.author)
        print (message.content)

        prompt_bienvenida = f"""Dale una bienvenida a {str(message.author)[:-5]} 
        de parte del centro de graduados FIUBA (Facultad de ingenieria de la Universidad de Buenos Aires)
        y recomedale nuestros cursos tutorizados, con docentes en vivo , 
        basados en los mejores cursos de coursera y el apoyo de la comunidad, recomandando nuestras paginas http://www.graduadosfiuba.org y
        http://ia.tuexitoprofesional.guru, explayate en por que sirve el metodo de estudio en equipo y la ventaja de tener acceso a los mejores
        cursos del mundo. Por ultimo recorda que pueden consultar  gpt anteponiendo /bot a la consulta
        """

        if message.author == self.user:
            return 
        command , user_message = None, None

        if message.content.lower() in ["", "help","ayuda","/?","?"]:
            await message.channel.send(f"Bienvenido {str(message.author)[:-5]}\npara usar gpt antepone /bot a tu consulta")
                                       
        for text in ["/bot","/gpt","/chat"]:
            if message.content.startswith(text):
                command = message.content.split(" ")[0]
                user_message = message.content.replace(text,"")
                print("commando :",command, "\nmensaje :",user_message)
        
        if command in ["/bot","/gpt"]:
            if user_message == "":
                user_message = prompt_bienvenida     
            try:
                res = gpt(user_message)
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
        elif command == "/chat":
            res = chat(user_message)
            await message.channel.send(f"chat : {res}")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(discord_token)