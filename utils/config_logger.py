#src/logs/config_logger.py
import logging.config
import os
import json
import colorlog

def configurar_logging(default_path='src/logs/logging.json', default_level=logging.DEBUG, env_key='LOG_CFG'):
    """Configura el logging basado en un archivo JSON."""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level, handlers=[colorlog_handler()])
    
    return logging.getLogger(__name__)

def colorlog_handler():
    """Crea un manejador de colorlog."""
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s\n",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    ))
    return handler

class InfoErrorFilter(logging.Filter):
    def filter(self, record):
        # Permitir solo registros de nivel INFO y ERROR
        return record.levelno in (logging.INFO, logging.ERROR)

# Configurar el logger con un nivel específico
configurar_logging()
