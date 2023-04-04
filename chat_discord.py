import discord 
from dotenv import load_dotenv
import os
import openai


load_dotenv()

discord_token = (os.getenv("bot_key"))
openai_key = os.getenv("gpt_key")

openai.api_key = openai_key

def gpt(entrada):
    completion = openai.ChatCompletion.create(
                    model       = "gpt-3.5-turbo", 
                    messages    = [{"role": "user", "content": entrada}],
                    temperature = 1,
                    max_tokens  = 2048)
    
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

        if message.author == self.user:
            return 
        command , user_message = None, None

        if message.content == "" or message.content.lower() == "help" or message.content.lower() == "ayuda":
             await message.channel.send(f"Bienvenido {message.author} para usar gpt antepone /bot a tu consulta")
                                       
        for text in ["/bot","/gpt","/chat"]:
            if message.content.startswith(text):
                command = message.content.split(" ")[0]
                user_message = message.content.replace(text,"")
                # print("commando :",command, user_message)
        
        if command in ["/bot","/gpt"]:
            res = gpt(user_message)
            await message.channel.send(f"chat : {res}")
        elif command == "/chat":
            res = chat(user_message)
            await message.channel.send(f"chat : {res}")

intents = discord.Intents.default()
intents.message_content = True


client = MyClient(intents=intents)

client.run(discord_token)