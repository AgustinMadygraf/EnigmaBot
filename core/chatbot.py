# core/chatbot.py
from typing import Callable
from gpt4all import GPT4All
from utils.config_logger import configurar_logging
from utils.ram_selector import RamSelector
from utils.model_selector import ModelSelector
from utils.system_template_selector import SystemTemplateSelector
from tabulate import tabulate
import time
import asyncio

logger = configurar_logging()

class ChatBot:
    def __init__(self, config, model_class=GPT4All, input_func: Callable = input):
        self.config = config
        self.input_func = input_func
        self.ram_selector = RamSelector(config, input_func)
        self.ram_seleccionada = self.ram_selector.seleccionar_memoria_ram()
        self.model_selector = ModelSelector(config, self.ram_seleccionada, input_func, logger)
        self.modelo_seleccionado = self.model_selector.seleccionar_modelo()
        self.system_template_selector = SystemTemplateSelector(config, input_func, logger)
        self.system_template = self.system_template_selector.seleccionar_system_template()
        self.model_path = config['model_path']
        self.model_class = model_class
        self.model = self.model_class(self.modelo_seleccionado, self.model_path)
        self.chat_histories = {}
        self.monitor_task = None

    def seleccionar_memoria_ram(self):
        """
        Solicita al usuario seleccionar la capacidad de memoria RAM.
        """
        ram_options = self.config['ram_options']
        table_data = [[key, value] for key, value in ram_options.items()]
        table = tabulate(table_data, headers=["Opción", "Memoria RAM"], tablefmt="grid")
        print(table)

        opcion_ram = self.input_func("\nElige una opción: ")
        if opcion_ram == "":
            opcion_ram = "4"
        logger.info(f"Opción de RAM seleccionada: {opcion_ram}")
        return ram_options.get(opcion_ram, "2")

    def seleccionar_modelo(self):
        """
        Permite al usuario seleccionar un modelo de IA basado en la capacidad de RAM seleccionada.
        """
        modelos_a_mostrar = self.obtener_modelos_disponibles()
        self.mostrar_opciones_modelo(modelos_a_mostrar)
        return self.obtener_seleccion_modelo(modelos_a_mostrar)

    def obtener_modelos_disponibles(self):
        """
        Obtiene la lista de modelos disponibles según la RAM seleccionada.
        """
        return self.config['models_available'].get(self.ram_seleccionada, [])

    def mostrar_opciones_modelo(self, modelos):
        """
        Muestra los modelos de IA disponibles al usuario.
        """
        if modelos:
            logger.info("Modelos disponibles:")
            table_data = [[idx + 1, modelo] for idx, modelo in enumerate(modelos)]
            table = tabulate(table_data, headers=["#", "Modelo"], tablefmt="grid")
            print(table)

    def obtener_seleccion_modelo(self, modelos):
        """
        Obtiene la selección del usuario de entre los modelos disponibles.
        """
        while True:
            try:
                seleccion_numero = self.input_func("\nSelecciona el número del modelo: ").strip()
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

    def seleccionar_system_template(self):
        """
        Permite al usuario seleccionar un template de sistema para el chatbot.
        """
        system_templates = self.config['system_templates']
        table_data = [[idx + 1, template['mode']] for idx, template in enumerate(system_templates)]
        table = tabulate(table_data, headers=["#", "Modo"], tablefmt="grid")
        print(table)

        while True:
            try:
                seleccion_numero = self.input_func("\nSelecciona el número del template de sistema: ").strip()
                if seleccion_numero == "":
                    seleccion_numero = "1"
                seleccion_numero = int(seleccion_numero)
                if 1 <= seleccion_numero <= len(system_templates):
                    system_template = system_templates[seleccion_numero - 1]['template']
                    logger.info(f"Template de sistema seleccionado: {system_templates[seleccion_numero - 1]['mode']}")
                    return system_template
                else:
                    print("Selección fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Por favor ingresa un número.")

    async def iniciar_chat(self):
        logger.info("Bienvenido al ChatBot interactivo!")
        chat_id = "user_console"
        self.preparar_chat(chat_id)
        await self.ciclo_principal_chat(chat_id)

    def preparar_chat(self, chat_id):
        """
        Prepara el entorno de chat inicializando el historial de chat.
        """
        self.chat_histories[chat_id] = []

    async def ciclo_principal_chat(self, chat_id):
        """
        Ejecuta el ciclo principal del chat interactivo.
        """
        while True:
            mensaje = await self.obtener_input_async("User: ")
            if mensaje.lower() == "salir":
                logger.info("Terminando el chat. ¡Hasta luego!")
                break
            self.procesar_mensaje(chat_id, mensaje)

    async def obtener_input_async(self, prompt):
        """
        Solicita entrada del usuario de manera asíncrona.
        """
        print(prompt, end='', flush=True)
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, input)

    def procesar_mensaje(self, chat_id, mensaje):
        self.chat_histories[chat_id].append({'role': 'user', 'content': mensaje})
        respuesta = self.generar_respuesta(chat_id)
        print("")
        logger.info(f"Bot: {respuesta}")

    def generar_respuesta(self, chat_id):
        logger.info(f"Consultando a la IA local, CPU trabajando...")
        inicio_generacion = time.time()
        prompt = self.construir_prompt(chat_id)
        respuesta = self.obtener_respuesta(prompt)
        self.registrar_respuesta(chat_id, respuesta)
        tiempo_generacion = time.time() - inicio_generacion
        print("")
        logger.info(f"Tiempo de generación de respuesta: {tiempo_generacion:.2f} segundos")
        return respuesta

    def construir_prompt(self, chat_id):
        """
        Construye el prompt basado en el historial de chat.
        """
        chat_history = self.chat_histories[chat_id]
        return " ".join([msg['content'] for msg in chat_history])

    def obtener_respuesta(self, prompt):
        """
        Obtiene la respuesta del modelo IA.
        """
        tokens = []
        with self.model.chat_session(self.system_template):
            for token in self.model.generate(prompt, streaming=True):
                tokens.append(token)
                print(token, end='', flush=True)
        return "".join(tokens)

    def registrar_respuesta(self, chat_id, respuesta):
        """
        Registra la respuesta en el historial de chat.
        """
        self.chat_histories[chat_id].append({'role': 'bot', 'content': respuesta})
