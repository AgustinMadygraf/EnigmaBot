# src/config_loader.py
import os
import json
import sys
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.cargar_configuracion()

    def cargar_configuracion(self):
        """
        Inicializa y carga la configuración del programa.
        Retorna un objeto de configuración.
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                logger.info("Configuración cargada correctamente.")
                return config
        except FileNotFoundError:
            logger.error(f"Archivo '{self.config_file}' no encontrado.")
            sys.exit("Error: Archivo de configuración no encontrado.")
        except json.JSONDecodeError:
            logger.error(f"Error al decodificar '{self.config_file}'. Verifica el formato del archivo.")
            sys.exit("Error: Formato de archivo de configuración inválido.")
        except Exception as e:
            logger.error(f"Error inesperado al cargar '{self.config_file}': {e}")
            sys.exit("Error inesperado al cargar la configuración.")
