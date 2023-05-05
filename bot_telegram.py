from dotenv import load_dotenv
import os
import openai
from collections import deque
#from telegram.ext import Updater,  CommandHandler , MessageHandler, filters

load_dotenv()

token = os.environ.get('telegram')

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

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


async def bot(update:Update, context:ContextTypes.DEFAULT_TYPE):
    mensage = update.to_dict()['message']["text"][4:]
    print(mensage)
    usuario = update.effective_user.first_name
    respuesta = gpt(usuario,mensage)
    print(respuesta)
    await update.message.reply_text(respuesta)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #print(dir(context))
    #print(context.chat_data)
    print(*update.to_dict().items(), sep="\n")
    print(update.to_dict()["message"]["text"])

    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("bot", bot))

app.run_polling()

