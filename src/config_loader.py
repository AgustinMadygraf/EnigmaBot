# src/config_loader.py
import os
import json
import sys
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.cargar_configuracion_inicial()

    def cargar_configuracion_inicial(self):
        """
        Inicializa y carga la configuración inicial del programa.
        Retorna un objeto de configuración.
        """
        try:
            config = self.cargar_configuracion(self.config_file)
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

    def cargar_configuracion(self, ruta_archivo):
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
