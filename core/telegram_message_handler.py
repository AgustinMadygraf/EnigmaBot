#EnigmaBot/core/telegram_message_handler.py
from telegram import Update
from telegram.ext import CallbackContext
from core.chatbot import ChatBot

class TelegramMessageHandler:
    """Class to handle Telegram messages."""

    def __init__(self, chatbot: ChatBot):
        """
        Initialize the message handler.

        :param chatbot: The ChatBot instance to process and generate responses.
        """
        self.chatbot = chatbot

    def echo(self, update: Update, context: CallbackContext) -> None:
        """
        Echo the user's message by processing it through the chatbot.

        :param update: The update object containing the user's message.
        :param context: The context object containing information about the chat.
        """
        user_message = update.message.text
        self.chatbot.procesar_mensaje("telegram_user", user_message)
        response = self.chatbot.generar_respuesta("telegram_user")
        update.message.reply_text(response)
