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
    ram_seleccionada = seleccionar_memoria_ram(config)
    seleccion_modelo = seleccionar_modelo(config, ram_seleccionada)

    if seleccion_modelo:
        model = await initialize_ai_model(config, seleccion_modelo)
        if model:
            # Crear instancia de ChatBot para la consola
            logger.info(f"selected model: {seleccion_modelo}")
            logger.info(f"model path: {config['model_path']}")
            chatbot = ChatBot(seleccion_modelo, config['model_path'])
            chatbot.iniciar_chat()
        else:
            logger.warning("No se pudo inicializar el modelo.")
    else:
        logger.warning("No se ha inicializado ningún modelo.")