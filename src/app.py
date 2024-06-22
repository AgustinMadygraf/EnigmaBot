# src/app.
import sys
from src.config_loader import ConfigManager
from src.chatbot import ChatBot  
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

async def main():
    config_manager = ConfigManager()
    config = config_manager.config
    logger.debug(f"Configuración cargada: {config}\n")
    logger.debug(f"Versión de Python: {sys.version}")
    logger.debug(f"El archivo seleccionado para trabajar es: {config['chat_history_path']}")
    chatbot = ChatBot(config)
    await chatbot.iniciar_chat()
