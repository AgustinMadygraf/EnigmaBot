# src/app.py
import sys
from src.config_loader import cargar_configuracion_inicial
from src.chatbot import ChatBot  
from src.logs.config_logger import configurar_logging
import asyncio

logger = configurar_logging()

async def main():
    config = cargar_configuracion_inicial()
    logger.debug(f"Configuración cargada: {config}\n")
    logger.debug(f"Versión de Python: {sys.version}")
    chatbot = ChatBot(None, config['model_path'], config)
    await chatbot.iniciar_chat()
