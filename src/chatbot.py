# src/chatbot.py

from gpt4all import GPT4All
from src.logs.config_logger import configurar_logging

logger = configurar_logging()

class ChatBot:
    def __init__(self, model_name, model_path):
        self.model = GPT4All(model_name, model_path)
        self.chat_histories = {}

    def iniciar_chat(self):
        logger.info("Bienvenido al ChatBot interactivo!")
        chat_id = "user_console"  # Usaremos un ID ficticio para la consola
        self.chat_histories[chat_id] = []
        while True:
            mensaje = input("User: ")
            if mensaje.lower() == "salir":
                logger.info("Terminando el chat. ¡Hasta luego!")
                break
            self.procesar_mensaje(chat_id, mensaje)

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
        for token in self.model.generate(prompt, temp=0.7,streaming=True):
            tokens.append(token)
            print(token, end='', flush=True)
        respuesta = "".join(tokens)
        self.chat_histories[chat_id].append({'role': 'bot', 'content': respuesta})
        return respuesta
