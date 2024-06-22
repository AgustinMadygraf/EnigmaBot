# src/app.py
import sys
from src.config_loader import cargar_configuracion_inicial
from src.user_interaction_manager import obtener_opciones_usuario, seleccionar_modelo, initialize_ai_model
from src.logs.config_logger import configurar_logging
from src.chatbot import ChatBot  

logger = configurar_logging()

async def main():
    config = cargar_configuracion_inicial()
    logger.info(f"Configuración cargada: {config}\n")
    logger.info(f"Versión de Python: {sys.version}")
    logger.info(f"El archivo seleccionado para trabajar es: {config['chat_history_path']}")

    # Obtener opciones del usuario
    quick_response, ram_seleccionada = obtener_opciones_usuario(config)
    seleccion_modelo = seleccionar_modelo(config, ram_seleccionada)

    if seleccion_modelo:
        model = await initialize_ai_model(config, seleccion_modelo)
        if model:
            # Crear instancia de ChatBot para la consola
            chatbot = ChatBot(seleccion_modelo, config['model_path'])
            chatbot.iniciar_chat()
        else:
            logger.warning("No se pudo inicializar el modelo.")
    else:
        logger.warning("No se ha inicializado ningún modelo.")