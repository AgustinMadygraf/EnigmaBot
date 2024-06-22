#Telegram_Chatbot/src/config/config_loader.py
import os
import json
import sys
from dotenv import load_dotenv
from tabulate import tabulate
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

def cargar_configuracion_inicial():
    """
    Inicializa y carga la configuración inicial del programa.
    Retorna un objeto de configuración.
    """
    # Configuración del logger
    print("")
    # Cargar configuración desde un archivo JSON
    try:
        config = cargar_configuracion('config.json')
        logger.debug("Configuración cargada correctamente.")
    except FileNotFoundError:
        logger.error("Archivo 'config.json' no encontrado.")
        sys.exit("Error: Archivo de configuración no encontrado.")
    except json.JSONDecodeError:
        logger.error("Error al decodificar 'config.json'. Verifica el formato del archivo.")
        sys.exit("Error: Formato de archivo de configuración inválido.")
    except Exception as e:
        logger.error(f"Error inesperado al cargar 'config.json': {e}")
        sys.exit("Error inesperado al cargar la configuración.")

    return config

def cargar_configuracion(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        logger.error(f"Archivo '{ruta_archivo}' no encontrado.")
        sys.exit("Error: Archivo de configuración no encontrado.")
    except json.JSONDecodeError:
        logger.error(f"Error al decodificar '{ruta_archivo}'. Verifica el formato del archivo.")
        sys.exit("Error: Formato de archivo de configuración inválido.")
    except Exception as e:
        logger.error(f"Error inesperado al cargar '{ruta_archivo}': {e}")
        sys.exit("Error inesperado al cargar la configuración.")
