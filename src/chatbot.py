# src/chatbot.py

from gpt4all import GPT4All

class ChatBot:
    def __init__(self, model_name, model_path):
        self.model = GPT4All(model_name, model_path)
        self.chat_histories = {}

    def iniciar_chat(self):
        print("Bienvenido al ChatBot interactivo!")
        chat_id = "user_console"  # Usaremos un ID ficticio para la consola
        self.chat_histories[chat_id] = []
        while True:
            mensaje = input("Tú: ")
            if mensaje.lower() == "salir":
                print("Terminando el chat. ¡Hasta luego!")
                break
            self.procesar_mensaje(chat_id, mensaje)

    def procesar_mensaje(self, chat_id, mensaje):
        self.chat_histories[chat_id].append({'role': 'user', 'content': mensaje})
        respuesta = self.generar_respuesta(chat_id)
        print(f"Bot: {respuesta}")

    def generar_respuesta(self, chat_id):
        chat_history = self.chat_histories[chat_id]
        prompt = " ".join([msg['content'] for msg in chat_history])
        respuesta = self.model.generate(prompt, temp=0.7)
        self.chat_histories[chat_id].append({'role': 'bot', 'content': respuesta})
        return respuesta
