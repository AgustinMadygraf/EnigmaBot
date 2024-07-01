#EnigmaBot/core/main.py
import sys
import asyncio
from utils.config_loader import ConfigManager
from core.chatbot import ChatBot
from core.telegram_bot import iniciar_chat_telegram
from gpt4all import GPT4All
from dotenv import load_dotenv
from logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()
# Cargar las variables del archivo .env
load_dotenv()

async def main(config_file="config/config.json", input_func=input, model_class=GPT4All):
    config_manager = ConfigManager(config_file)
    config = config_manager.config
    logger.debug(f"Configuración cargada: {config}\n")
    logger.debug(f"Versión de Python: {sys.version}")
    logger.info(f"El archivo seleccionado para trabajar es: {config['chat_history_path']}")

    # Preguntar al usuario si quiere conversar o entrenar
    choice = input_func("¿Deseas conversar con el ChatBot (1) o entrenarlo (2)? [1/2]: ").strip()
    if choice == "2":
        await entrenar_chatbot(config, input_func, model_class)
    else:
        platform_choice = input_func("¿Deseas conversar por consola (1) o por Telegram (2)? [1/2]: ").strip()
        if platform_choice == "2":
            await iniciar_chat_telegram(config, input_func, model_class)
        else:
            chatbot = ChatBot(config, model_class=model_class, input_func=input_func)
            await chatbot.iniciar_chat()

async def entrenar_chatbot(config, input_func, model_class):
    chatbot = ChatBot(config, model_class=model_class, input_func=input_func)
    await chatbot.entrenar()

def run_main():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.ensure_future(main())
    else:
        loop.run_until_complete(main())
