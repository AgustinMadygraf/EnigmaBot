# src/config_loader.py
import json
import sys
from logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

class ConfigManager:
    def __init__(self, config_file, logger=logger):
        self.config_file = config_file
        self.logger = logger
        self.config = self.cargar_configuracion()

    def cargar_configuracion(self):
        """
        Inicializa y carga la configuración del programa.
        Retorna un objeto de configuración.
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                self.logger.info("Configuración cargada correctamente.")
                return config
        except FileNotFoundError:
            self.manejar_error(f"Archivo '{self.config_file}' no encontrado.", "Error: Archivo de configuración no encontrado.")
        except json.JSONDecodeError as e:
            self.manejar_error(f"Error al decodificar '{self.config_file}': {e}", "Error: Formato de archivo de configuración inválido.")
        except PermissionError:
            self.manejar_error(f"Permiso denegado al intentar leer el archivo '{self.config_file}'.", "Error: Permiso denegado.")
        except Exception as e:
            self.manejar_error(f"Error inesperado al cargar '{self.config_file}': {e}", "Error inesperado al cargar la configuración.")

    def manejar_error(self, mensaje_log, mensaje_salida):
        """
        Maneja los errores de configuración registrando el mensaje de error y finalizando el programa.
        """
        self.logger.error(mensaje_log)
        sys.exit(mensaje_salida)
