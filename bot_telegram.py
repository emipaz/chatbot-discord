from dotenv import load_dotenv
import os
# https://python-telegram-bot.org/
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from chatgpt import gpt
from prompt import comandos

load_dotenv()

token = os.environ.get('telegram')

async def bot(update:Update, context:ContextTypes.DEFAULT_TYPE):
    _ , mensage = update.to_dict()['message']["text"].split(maxsplit=1)
    print(mensage)
    
    usuario = update.effective_user.first_name
    comando, mensage2 = mensage.split(maxsplit=1)
    print(comando)
    
    if comando in comandos:
        consulta = comandos[comando] + mensage2
    else:
        consulta = mensage
    
    respuesta = gpt(usuario,consulta)
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

