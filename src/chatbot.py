# src/chatbot.py

from gpt4all import GPT4All
from src.logs.config_logger import configurar_logging
from tabulate import tabulate
import time

logger = configurar_logging()

class ChatBot:
    def __init__(self, config):
        self.config = config
        self.ram_seleccionada = self.seleccionar_memoria_ram()
        self.modelo_seleccionado = self.seleccionar_modelo()
        self.model_path = config['model_path']
        self.model = GPT4All(self.modelo_seleccionado, self.model_path)
        self.chat_histories = {}
        self.monitor_task = None
        self.system_template = self.seleccionar_system_template()

    def seleccionar_memoria_ram(self):
        """
        Solicita al usuario seleccionar la capacidad de memoria RAM.
        """
        ram_options = self.config['ram_options']
        table_data = [[key, value] for key, value in ram_options.items()]
        table = tabulate(table_data, headers=["Opción", "Memoria RAM"], tablefmt="grid")
        print(table)

        opcion_ram = input("\nElige una opción: ")
        if opcion_ram == "":
            opcion_ram = "4"
        logger.info(f"Opción de RAM seleccionada: {opcion_ram}")
        return ram_options.get(opcion_ram, "2")

    def seleccionar_modelo(self):
        """
        Permite al usuario seleccionar un modelo de IA basado en la capacidad de RAM seleccionada.
        """
        modelos_a_mostrar = self.config['models_available'].get(self.ram_seleccionada, [])
        self.mostrar_opciones_modelo(modelos_a_mostrar)

        return self.obtener_seleccion_modelo(modelos_a_mostrar)

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
                seleccion_numero = input("\nSelecciona el número del template de sistema: ").strip()
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
        chat_id = "user_console"  # Usaremos un ID ficticio para la consola
        self.chat_histories[chat_id] = []
        try:
            while True:
                mensaje = input("User: ")
                if mensaje.lower() == "salir":
                    logger.info("Terminando el chat. ¡Hasta luego!")
                    break
                self.procesar_mensaje(chat_id, mensaje)
        finally:
            await self.detener_monitorizacion()

    def procesar_mensaje(self, chat_id, mensaje):
        self.chat_histories[chat_id].append({'role': 'user', 'content': mensaje})
        respuesta = self.generar_respuesta(chat_id)
        print("")
        logger.info(f"Bot: {respuesta}")

    def generar_respuesta(self, chat_id):
        logger.info(f"Consultando a la IA local, CPU trabajando...")
        inicio_generacion = time.time()
        tokens = []
        chat_history = self.chat_histories[chat_id]
        prompt = " ".join([msg['content'] for msg in chat_history])
        with self.model.chat_session(self.system_template):
            for token in self.model.generate(prompt, streaming=True):
                tokens.append(token)
                print(token, end='', flush=True)
            respuesta = "".join(tokens)
            self.chat_histories[chat_id].append({'role': 'bot', 'content': respuesta})
            tiempo_generacion = time.time() - inicio_generacion
            logger.info(f"\nTiempo de generación de respuesta: {tiempo_generacion:.2f} segundos")
            return respuesta


