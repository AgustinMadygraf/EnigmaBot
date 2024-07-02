#EnigmaBot/core/telegram_bot.py
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from core.chatbot import ChatBot
from core.telegram_command_handler import TelegramCommandHandler
from core.telegram_message_handler import TelegramMessageHandler
import os
from logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

class TelegramBot:
    """Clase principal para ejecutar el bot de Telegram."""

    def __init__(self, config, input_func=input):
        """
        Inicializa el bot de Telegram.

        :param config: Diccionario de configuración.
        :param input_func: Función de entrada, por defecto es la función input de Python.
        """
        self.config = config
        self.chatbot = ChatBot(config, input_func=input_func)
        self.token = os.getenv("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("No se encontró TELEGRAM_TOKEN en las variables de entorno")

        self.command_handler = TelegramCommandHandler()
        self.message_handler = TelegramMessageHandler(self.chatbot)
        
        logger.debug("TelegramBot inicializado con config: %s y token: %s", config, self.token)

    async def run(self):
        """
        Ejecuta el bot de Telegram.
        """
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", self.command_handler.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler.echo))

        await application.initialize()
        await application.start()
        logger.debug("Bot de Telegram iniciado...")
        
        await application.updater.start_polling()
        await application.updater.idle()

async def iniciar_chat_telegram(config, input_func, model_class):
    """
    Inicia el bot de chat de Telegram.

    :param config: Diccionario de configuración.
    :param input_func: Función de entrada, por defecto es la función input de Python.
    :param model_class: Clase del modelo para el chatbot.
    """
    telegram_bot = TelegramBot(config, input_func=input_func)
    await telegram_bot.run()
