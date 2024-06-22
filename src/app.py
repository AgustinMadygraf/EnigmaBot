from src.logs.config_logger import configurar_logging

#config_manager = ConfigManager()  
logger = configurar_logging()

def main():
    """
    Función principal para iniciar el chatbot de Telegram.

    Esta función se encarga de inicializar el entorno de ejecución, configurar la sesión de usuario y 
    gestionar el ciclo principal de ejecución del chatbot. Incluye la configuración de logger, la obtención de 
    opciones de usuario, la selección del modelo de IA y la ejecución del ciclo principal de mensajes.

    Parámetros:
    Ninguno

    Retorna:
    None
    """
    logger.debug(f"Configuración cargada: {config}\n")
    logger.debug(f"Versión de Python: {sys.version}")
    logger.debug(f"El archivo seleccionado para trabajar es: {config['chat_history_path']}")
    user_id_str = str(593052206) #Queda pendiente automatizar el proceso de obtención de ID de usuario
    quick_response, ram_seleccionada = obtener_opciones_usuario(config)
    seleccion_modelo = seleccionar_modelo(config, ram_seleccionada)
    if seleccion_modelo:
        model = await initialize_ai_model(config, seleccion_modelo)
        if model:
            await run_main_cycle(model, config, user_id_str, seleccion_modelo, quick_response)
        else:
            logger.warning("No se pudo inicializar el modelo.")
    else:
        logger.warning("No se ha inicializado ningún modelo.")