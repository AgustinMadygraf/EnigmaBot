# src/user_interaction_manager.py

import sys
from tabulate import tabulate
import psutil
import asyncio
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

# Función para recolectar datos de recursos
def recolectar_datos_recursos(velocidad_base_ghz=3.7):
    """Recolecta y devuelve datos de los recursos del sistema."""
    disk_io_c = psutil.disk_io_counters(perdisk=True).get('G:')
    disk_io_d = psutil.disk_io_counters(perdisk=True).get('E:')  

    datos = {
        'ram_usada_gb': psutil.virtual_memory().used / (1024 ** 3),                           # Convertir a GB
        'ram_total_gb': psutil.virtual_memory().total / (1024 ** 3),                          # Convertir a GB
        'ram_porcenta': psutil.virtual_memory().percent,                                      # Porcentaje de uso
        'cpu_frecue_b': velocidad_base_ghz,                                                   # Frecuencia base del procesador
        'cpu_frecue_a': round(psutil.cpu_percent(interval=1) * velocidad_base_ghz / 100, 2),  # Frecuencia actual del procesador
        'cpu_porcenta': psutil.cpu_percent(interval=1),                                       # Porcentaje de uso
        'c:_vel_lect': disk_io_c.read_bytes / (1024 ** 2) if disk_io_c else 0,                # Velocidad de lectura del disco C en MB
        'c:time_acti': disk_io_c.read_time / 1000 if disk_io_c else 0,                        # Tiempo de actividad del disco C en segundos
        'd:_vel_lect': disk_io_d.read_bytes / (1024 ** 2) if disk_io_d else 0,                # Velocidad de lectura del disco D en MB
        'd:time_acti': disk_io_d.read_time / 1000 if disk_io_d else 0                         # Tiempo de actividad del disco D en segundos
    }
    return datos

# Función para imprimir datos de recursos
def imprimir_datos_recursos(datos, primera_lectura=True):
    """Imprime los datos de los recursos en formato de tabla."""
    headers = ['RAM (GB)', 'CPU Frec. (GHz)', 'Disco C (GB)', 'Disco E (GB)']
    data = [
        ['Usado', f"{datos['ram_usada_gb']:.2f}", f"{datos['cpu_frecue_b']} GHz", f"{datos['c:_vel_lect']} kB/S", f"{datos['d:_vel_lect']} kB/S"],
        ['Total', f"{datos['ram_total_gb']:.2f}", f"{datos['cpu_frecue_b']} GHz", "N/A", "N/A"],
        ['Porcentaje de Uso', f"{datos['ram_porcenta']:.2f}%", f"{datos['cpu_porcenta']:.2f}%", f"{datos['c:time_acti']} %", f"{datos['d:time_acti']} %"]
    ]

    mensaje = "Primera lectura antes de la carga del LLM" if primera_lectura else "Lectura durante el proceso de carga del LLM"
    print(f"\n{mensaje}\n" + tabulate(data, headers, tablefmt="grid"))
    sys.stdout.flush()

# Función para monitorizar recursos
async def monitorizar_recursos(velocidad_base_ghz=3.7):
    primera_lectura = True
    while True:
        try:
            logger.debug("Recolectando datos de recursos...")
            datos_recursos = recolectar_datos_recursos(velocidad_base_ghz)
            imprimir_datos_recursos(datos_recursos, primera_lectura)
            primera_lectura = False  
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.debug("Monitorización de recursos finalizada.")
            break
        except Exception as e:
            logger.error(f"Error en la monitorización de recursos: {e}")
