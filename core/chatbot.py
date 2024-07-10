#EnigmaBor/core/chatbot.py
from typing import Callable
from gpt4all import GPT4All
from utils.ram_selector import RamSelector
from utils.model_selector import ModelSelector
from utils.system_template_selector import SystemTemplateSelector
from tabulate import tabulate
import time
import asyncio
from utils.database import connect_to_database
from logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

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
        self.session_id = self.create_new_session()

    def create_new_session(self):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions () VALUES ()")
        conn.commit()
        session_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return session_id

    def save_message_to_db(self, role, content):
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO chat_history (session_id, role, content) 
        VALUES (%s, %s, %s)
        """, (self.session_id, role, content))
        conn.commit()
        cursor.close()
        conn.close()

    def seleccionar_modelo(self):
        modelos_a_mostrar = self.obtener_modelos_disponibles()
        self.mostrar_opciones(modelos_a_mostrar, "Modelos disponibles:")
        return self.obtener_seleccion(modelos_a_mostrar, "\nSelecciona el número del modelo: ")

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
        system_templates = self.config['system_templates']
        self.mostrar_opciones(system_templates, "Templates de sistema disponibles:", lambda x: x['mode'])
        seleccion = self.obtener_seleccion(system_templates, "\nSelecciona el número del template de sistema: ")
        return seleccion['template']

    def mostrar_opciones(self, opciones, mensaje, key_func=lambda x: x):
        if opciones:
            logger.info(mensaje)
            table_data = [[idx + 1, key_func(opcion)] for idx, opcion in enumerate(opciones)]
            table = tabulate(table_data, headers=["#", "Opción"], tablefmt="grid")
            print(table)

    def obtener_seleccion(self, opciones, mensaje_seleccion):
        while True:
            try:
                seleccion_numero = self.input_func(mensaje_seleccion).strip()
                if seleccion_numero == "":
                    seleccion_numero = "1"
                seleccion_numero = int(seleccion_numero)
                if 1 <= seleccion_numero <= len(opciones):
                    seleccion = opciones[seleccion_numero - 1]
                    logger.info(f"Selección: {seleccion}")
                    return seleccion
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
            mensaje = await self.obtener_input_async("Human: ")
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
        self.guardar_mensaje_si_nuevo(chat_id, 'Human', mensaje)
        respuesta = self.generar_respuesta(chat_id)
        print("")
        logger.info(f"Assistant: {respuesta}")
        self.registrar_respuesta(chat_id, respuesta)

    def guardar_mensaje_si_nuevo(self, chat_id, role, mensaje):
        if not self.chat_histories[chat_id] or self.chat_histories[chat_id][-1]['content'] != mensaje or self.chat_histories[chat_id][-1]['role'] != role:
            self.chat_histories[chat_id].append({'role': role, 'content': mensaje})
            self.save_message_to_db(role, mensaje)

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
        prompt_parts = []
        is_first_message = True
        for msg in chat_history:
            role = msg['role']
            if role == 'Human':
                if is_first_message:
                    prompt_parts.append(f"{msg['content']}\n")
                    is_first_message = False
                else:
                    prompt_parts.append(f"### Human:\n{msg['content']}\n")
            elif role == 'Assistant':
                prompt_parts.append(f"### Assistant:\n{msg['content']}\n")
        return "\n".join(prompt_parts)

    def obtener_respuesta(self, prompt):
        """
        Obtiene la respuesta del modelo IA.
        """
        tokens = []
        with self.model.chat_session(self.system_template):
            print(f"Prompt: {prompt}")
            for token in self.model.generate(prompt, max_tokens=2048, streaming=True,n_batch = 9):
                tokens.append(token)
                print(token, end='', flush=True)
        return "".join(tokens)

    def registrar_respuesta(self, chat_id, respuesta):
        if not self.chat_histories[chat_id] or self.chat_histories[chat_id][-1]['content'] != respuesta or self.chat_histories[chat_id][-1]['role'] != 'Assistant':
            self.chat_histories[chat_id].append({'role': 'Assistant', 'content': respuesta})
            self.save_message_to_db('Assistant', respuesta)

    # Función de entrenamiento del chatbot
    async def entrenar(self):
        logger.info("Iniciando el proceso de entrenamiento del ChatBot.")
        # Aquí puedes añadir el código para el proceso de entrenamiento del ChatBot.
        print("Entrenando el ChatBot...")
        await asyncio.sleep(1)  # Simulación de entrenamiento
        print("Entrenamiento completado.")
        logger.info("Entrenamiento del ChatBot completado.")