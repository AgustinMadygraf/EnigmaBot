#Telegram_chatbot\src\core\user_interaction_manager.py
import time
import sys
from gpt4all import GPT4All
from tabulate import tabulate
import psutil
import asyncio
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

def obtener_opciones_usuario(config):
    """
    Obtiene las opciones del usuario para la configuración del chatbot.

    Esta función interactúa con el usuario para determinar el modo de respuesta del bot y la capacidad de memoria RAM deseada. 
    Asegura que las opciones seleccionadas sean válidas según la configuración proporcionada.

    Parámetros:
    config (dict): Un diccionario que contiene la configuración del bot, incluyendo opciones de RAM.

    Retorna:
    tuple: Un tuple que contiene un booleano para indicar si se usa respuesta rápida y la memoria RAM seleccionada.
    """
    modo_respuesta = obtener_modo_respuesta()
    ram_seleccionada = seleccionar_memoria_ram(config)
    return modo_respuesta, ram_seleccionada

def obtener_modo_respuesta():
    """
    Solicita al usuario elegir el modo de respuesta del bot.

    Permite al usuario elegir entre una respuesta rápida o una respuesta detallada. Valida la entrada del usuario y 
    usa el modo de respuesta rápida por defecto en caso de una selección inválida.

    Retorna:
    bool: Verdadero para respuesta rápida, Falso para respuesta detallada.
    """
    print("\nElige el modo de respuesta del bot:")
    print("1. Respuesta rápida (ventana de contexto limitada a la última pregunta)")
    print("2. Respuesta detallada (ventana de contexto ampliada a todo el historial)")
    modo_respuesta = input("Selecciona una opción (1 o 2): ")
    if modo_respuesta == "":
        modo_respuesta = "1"
    logger.info(f"Modo de respuesta seleccionado: {modo_respuesta}")
    return modo_respuesta == "1" or modo_respuesta not in ["1", "2"]

def seleccionar_memoria_ram(config):
    """
    Solicita al usuario seleccionar la capacidad de memoria RAM.

    Permite al usuario elegir entre diferentes opciones de RAM disponibles en la configuración. 
    Valida la entrada del usuario y selecciona una opción predeterminada en caso de una selección inválida.

    Parámetros:
    config (dict): Un diccionario que contiene las opciones de RAM disponibles.

    Retorna:
    str: La capacidad de memoria RAM seleccionada.
    """
    ram_options = config['ram_options']
    table_data = [[key, value] for key, value in ram_options.items()]
    table = tabulate(table_data, headers=["Opción", "Memoria RAM"], tablefmt="grid")
    print(table)
    
    opcion_ram = input("\nElige una opción: ")
    if opcion_ram == "":
        opcion_ram = "3"
    logger.info(f"Opción de RAM seleccionada: {opcion_ram}")
    return ram_options.get(opcion_ram, "2")

def seleccionar_modelo(config, ram_seleccionada):
    """
    Permite al usuario seleccionar un modelo de IA basado en la capacidad de RAM seleccionada.

    Presenta al usuario una lista de modelos disponibles según la capacidad de RAM y permite seleccionar uno. 
    Asegura que la selección sea válida y maneja las entradas inválidas adecuadamente.

    Parámetros:
    config (dict): Un diccionario que contiene la configuración del bot, incluyendo los modelos disponibles.
    ram_seleccionada (str): La capacidad de RAM seleccionada por el usuario.

    Retorna:
    str: El modelo seleccionado o None si no se selecciona un modelo válido.
    """
    modelos_a_mostrar = config['models_available'].get(ram_seleccionada, [])
    mostrar_opciones_modelo(modelos_a_mostrar)

    return obtener_seleccion_modelo(modelos_a_mostrar)

def mostrar_opciones_modelo(modelos):
    """
    Muestra los modelos de IA disponibles al usuario.

    Parámetros:
    modelos (list): Una lista de modelos de IA disponibles.
    """
    if modelos:
        logger.info("Modelos disponibles:")
        table_data = [[idx + 1, modelo] for idx, modelo in enumerate(modelos)]
        table = tabulate(table_data, headers=["#", "Modelo"], tablefmt="grid")
        print(table)


def obtener_seleccion_modelo(modelos):
    """
    Obtiene la selección del usuario de entre los modelos disponibles.

    Parámetros:
    modelos (list): Una lista de modelos de IA disponibles.

    Retorna:
    str: El modelo seleccionado o None si la selección es inválida.
    """
    while True:
        try:
            seleccion_numero = input("\nSelecciona el número del modelo: ").strip()
            if seleccion_numero == "":
                seleccion_numero = "2"
            seleccion_numero = int(seleccion_numero)
            if 1 <= seleccion_numero <= len(modelos):
                modelo_seleccionado = modelos[seleccion_numero - 1]
                logger.info(f"Modelo seleccionado: {modelo_seleccionado}")
                return modelo_seleccionado
            else:
                print("Selección fuera de rango. Intenta de nuevo.")
        except ValueError:
            print("Entrada inválida. Por favor ingresa un número.")

async def initialize_ai_model(config, seleccion_modelo):
    loop = asyncio.get_event_loop()
    monitor_task = asyncio.create_task(monitorizar_recursos())
    try:
        inicio_carga = time.time()
        model = await loop.run_in_executor(None, cargar_modelo_sincrono, seleccion_modelo, config['model_path'])
        fin_carga = time.time()
        tiempo_carga = fin_carga - inicio_carga
        print("")
        logger.info(f"Modelo inicializado con éxito en {tiempo_carga:.2f} segundos.")
    except Exception as e:
        logger.error(f"Error al cargar el modelo: {e}")
    finally:
        monitor_task.cancel()
    return model

def cargar_modelo_sincrono(seleccion_modelo, model_path):
    return GPT4All(seleccion_modelo, model_path)

async def monitorizar_recursos():
    velocidad_base_ghz = 3.7 #Velocidad base del procesador en GHz
    primera_lectura = True
    while True:
        try:
            datos_recursos = recolectar_datos_recursos(velocidad_base_ghz)
            imprimir_datos_recursos(datos_recursos, primera_lectura)
            primera_lectura = False  
            await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.debug("Monitorización de recursos finalizada.")
            break

def recolectar_datos_recursos(velocidad_base_ghz):
    """ Recolecta y devuelve datos de los recursos del sistema. """
    disk_io_c = psutil.disk_io_counters(perdisk=True).get('G:')
    disk_io_d = psutil.disk_io_counters(perdisk=True).get('E:')  

    datos = {
        'ram_usada_gb'  : psutil.virtual_memory().used / (1024 ** 3),                           # Convertir a GB
        'ram_total_gb'  : psutil.virtual_memory().total / (1024 ** 3),                          # Convertir a GB
        'ram_porcenta'  : psutil.virtual_memory().percent,                                      # Porcentaje de uso

        'cpu_frecue_b'  : velocidad_base_ghz,                                                   # Frecuencia base del procesador
        'cpu_frecue_a'  : round(psutil.cpu_percent(interval=1) * velocidad_base_ghz / 100, 2),  # Frecuencia actual del procesador
        'cpu_porcenta'  : psutil.cpu_percent(interval=1),                                       # Porcentaje de uso

        'c:_vel_lect'   : disk_io_c.read_bytes / (1024 ** 2) if disk_io_c else 0,               # Velocidad de lectura del disco C en MB
        'c:time_acti'   : disk_io_c.read_time / 1000 if disk_io_c else 0,                       # Tiempo de actividad del disco C en segundos
        'd:_vel_lect'   : disk_io_d.read_bytes / (1024 ** 2) if disk_io_d else 0,               # Velocidad de lectura del disco D en MB
        'd:time_acti'   : disk_io_d.read_time / 1000 if disk_io_d else 0                        # Tiempo de actividad del disco D en segundos
    }
    return datos

def imprimir_datos_recursos(datos, primera_lectura): #aviso no funciona correctamente la funcion flush
    """ Imprime los datos de los recursos en formato de tabla. """
    headers = [             'RAM (GB)'                              , 'CPU Frec. (GHz)'                 , 'Disco C (GB)'                    , 'Disco E (GB)'                    ]
    data = [
        ['Usado'            , f"{datos['ram_usada_gb']:.2f}"        , f"{datos['cpu_frecue_b']} GHz"    , f"{datos['c:_vel_lect']} kB/S"    , f"{datos['d:_vel_lect']} kB/S"    ],
        ['Total'            , f"{datos['ram_total_gb']:.2f}"        , f"{datos['cpu_frecue_b']} GHz"    , "N/A"                             , "N/A"                             ],
        ['Porcentaje de Uso', f"{datos['ram_porcenta']:.2f}%"       , f"{datos['cpu_porcenta']:.2f}%"   , f"{datos['c:time_acti']} %"      , f"{datos['d:time_acti']} %"        ]
    ]
    
    if primera_lectura:
        mensaje = "Primera lectura antes de la carga del LLM"
        print(f"\n{mensaje}\n" + tabulate(data, headers, tablefmt="grid"))
 
    else: 
        mensaje= "Lectura durante el proceso de carga del LLM"
        sys.stdout.write(f"\n{mensaje}\n" + tabulate(data, headers, tablefmt="grid"))
        sys.stdout.flush()
    sys.stdout.write(" " * 150 + "\r")  
    sys.stdout.flush()

