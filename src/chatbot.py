# src/chatbot.py

from gpt4all import GPT4All
from src.logs.config_logger import configurar_logging
from tabulate import tabulate
import asyncio
import time
from src.user_interaction_manager import monitorizar_recursos

logger = configurar_logging()

class ChatBot:
    def __init__(self, model_name, model_path, config):
        self.config = config
        self.ram_seleccionada = self.seleccionar_memoria_ram()
        self.modelo_seleccionado = self.seleccionar_modelo()
        self.model = GPT4All(self.modelo_seleccionado, model_path)
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

    async def iniciar_chat(self):
        logger.info("Bienvenido al ChatBot interactivo!")
        chat_id = "user_console"  # Usaremos un ID ficticio para la consola
        self.chat_histories[chat_id] = []
        self.monitor_task = asyncio.create_task(self.iniciar_monitorizacion())
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
        tokens = []
        chat_history = self.chat_histories[chat_id]
        prompt = " ".join([msg['content'] for msg in chat_history])
        for token in self.model.generate(prompt, temp=0.7, streaming=True):
            tokens.append(token)
            print(token, end='', flush=True)
        respuesta = "".join(tokens)
        self.chat_histories[chat_id].append({'role': 'bot', 'content': respuesta})
        return respuesta

    async def generate_response(self, model, prompt):
        inicio_generacion = time.time()
        tokens = []
        logger.info("Invocando al modelo\n")

        if isinstance(prompt, list):
            prompt = ''.join([p['content'] for p in prompt])

        for token in model.generate(prompt, temp=0.7, streaming=True):
            tokens.append(token)
            print(token, end='', flush=True)

        tiempo_generacion = time.time() - inicio_generacion
        logger.info(f"\nTiempo de generación de respuesta: {tiempo_generacion:.2f} segundos")
        respuesta_bot = "".join(tokens)
        print(f"\n\nInicio Respuesta: \n{respuesta_bot}\nFin Respuesta\n\n\n")
        return respuesta_bot, tiempo_generacion

    async def iniciar_monitorizacion(self):
        self.monitor_task = asyncio.create_task(monitorizar_recursos())

    async def detener_monitorizacion(self):
        if self.monitor_task:
            self.monitor_task.cancel()
            await self.monitor_task
            logger.info("Monitorización de recursos detenida.")
