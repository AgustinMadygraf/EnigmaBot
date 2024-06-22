# src/app.py
import sys
from src.config_loader import cargar_configuracion_inicial
from src.user_interaction_manager import seleccionar_memoria_ram, seleccionar_modelo, initialize_ai_model
from src.chatbot import ChatBot  
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

async def main():
    config = cargar_configuracion_inicial()
    logger.debug(f"Configuración cargada: {config}\n")
    logger.debug(f"Versión de Python: {sys.version}")
    logger.debug(f"El archivo seleccionado para trabajar es: {config['chat_history_path']}")
    chatbot = ChatBot(None, config['model_path'], config)
    chatbot.iniciar_chat()
