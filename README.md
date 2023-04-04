# Bot de Discord con GPT-3

Este es un bot de Discord que utiliza la API de OpenAI para proporcionar respuestas en chat. El bot se ha configurado para utilizar el modelo GPT-3 y el modelo TextDavinci-003 para generar respuestas. 

## Requisitos

- Python 3.x
- Biblioteca externa Discord.py
- Biblioteca externa dotenv
- API Key para Discord y OpenAI

## Instalación

1. Clona este repositorio en tu máquina local.
2. Instala las bibliotecas externas utilizando los siguientes comandos: 

```bash
pip install discord.py
pip install python-dotenv
pip install openai
```

3. Crea una cuenta en [Discord Developer Portal](https://discord.com/developers/applications).
4. Crea una nueva aplicación en Discord Developer Portal y copia su token.
5. Crea una cuenta en [OpenAI](https://beta.openai.com/signup/).
6. Crea una nueva API Key en OpenAI y copia su token.
7. Crea un archivo `.env` en la carpeta principal del proyecto y agrega las siguientes líneas:
 ```
 bot_key=<token_de_discord>
 gpt_key=<token_de_openai>
 ```
 Reemplaza `<token_de_discord>` y `<token_de_openai>` con los tokens que copiaste anteriormente.  

8. Ejecuta el archivo `chat_discord.py` para comenzar a utilizar el bot.

## Uso

El bot tiene los siguientes comandos disponibles:

- `/bot`: utiliza el modelo GPT-3 para generar una respuesta basada en la entrada del usuario.
- `/chat`: utiliza el modelo TextDavinci-003 para generar una respuesta basada en la entrada del usuario.

## Contribución

Este proyecto es de código abierto y las contribuciones son bienvenidas. Si deseas contribuir, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una rama con tu nueva característica (`git checkout -b nueva_caracteristica`).
3. Haz tus cambios y haz commit (`git commit -m 'Agrega nueva característica'`).
4. Sube tus cambios (`git push origin nueva_caracteristica`).
5. Abre una pull request.

