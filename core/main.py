# core/main.py
import sys
import os
import asyncio
from utils.config_loader import ConfigManager
from core.chatbot import ChatBot
from utils.config_logger import configurar_logging
from gpt4all import GPT4All

logger = configurar_logging()

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
        chatbot = ChatBot(config, model_class=model_class, input_func=input_func)
        await chatbot.iniciar_chat()

async def entrenar_chatbot(config, input_func, model_class):
    chatbot = ChatBot(config, model_class=model_class, input_func=input_func)
    await chatbot.entrenar()

if __name__ == '__main__':
    asyncio.run(main())
