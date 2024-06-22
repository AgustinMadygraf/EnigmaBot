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

class ConfigManager:
    error_reported = False  # Indicador de error
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(ConfigManager, cls).__new__(cls)
        return cls.instance

    def __init__(self, config_file="config.json", setup_file="src/config/system_templates.json", default_model_path='E:\\Model _Explorer'):
        if not hasattr(self, 'initialized'):
            load_dotenv()
            self.config_data = self.load_json_file(config_file)
            self.telegram_token = os.getenv('TELEGRAM_TOKEN')
            self.model_path = os.getenv('MODEL_PATH', default_model_path)
            self.chat_history_path = self.config_data.get("chat_history_path", "data/context_window_telegram.json")
            self.initialized = True

    @staticmethod
    def load_json_file(file_path):
        try:
            with open(file_path, "r", encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Error al cargar '{file_path}': {e}")
        except Exception as e:
            logger.error(f"Error inesperado al cargar '{file_path}': {e}")
        return {}