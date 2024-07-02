#EnigmaBot/core/telegram_message_handler.py
from telegram import Update
from telegram.ext import CallbackContext
from core.chatbot import ChatBot
from logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

class TelegramMessageHandler:
    """Clase para manejar los mensajes de Telegram."""

    def __init__(self, chatbot: ChatBot):
        """
        Inicializa el manejador de mensajes.

        :param chatbot: La instancia de ChatBot para procesar y generar respuestas.
        """
        self.chatbot = chatbot
        logger.debug("TelegramMessageHandler inicializado con chatbot: %s", chatbot)

    def echo(self, update: Update, context: CallbackContext) -> None:
        """
        Repite el mensaje del usuario procesándolo a través del chatbot.

        :param update: El objeto update que contiene el mensaje del usuario.
        :param context: El objeto context que contiene información sobre el chat.
        """
        user_message = update.message.text
        logger.debug("Mensaje recibido del usuario: %s", user_message)
        
        self.chatbot.procesar_mensaje("telegram_user", user_message)
        response = self.chatbot.generar_respuesta("telegram_user")
        
        logger.debug("Respuesta generada por el chatbot: %s", response)
        update.message.reply_text(response)
