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
    chatbot = ChatBot(config, model_class=model_class, input_func=input_func)
    await chatbot.iniciar_chat()