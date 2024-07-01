#EnigmaBot/core/telegram_bot.py
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from core.chatbot import ChatBot
from core.telegram_command_handler import TelegramCommandHandler
from core.telegram_message_handler import TelegramMessageHandler
import os

class TelegramBot:
    """Main class to run the Telegram bot."""

    def __init__(self, config, input_func=input):
        """
        Initialize the Telegram bot.

        :param config: Configuration dictionary.
        :param input_func: Input function, default is Python's input function.
        """
        self.config = config
        self.chatbot = ChatBot(config, input_func=input_func)
        self.token = os.getenv("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("No TELEGRAM_TOKEN found in environment variables")

        self.command_handler = TelegramCommandHandler()
        self.message_handler = TelegramMessageHandler(self.chatbot)

    async def run(self):
        """
        Run the Telegram bot.
        """
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", self.command_handler.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler.echo))

        await application.initialize()
        await application.start()
        print("Bot de Telegram iniciado...")
        await application.updater.start_polling()
        await application.updater.idle()

async def iniciar_chat_telegram(config, input_func, model_class):
    """
    Start the Telegram chat bot.

    :param config: Configuration dictionary.
    :param input_func: Input function, default is Python's input function.
    :param model_class: Model class for the chatbot.
    """
    telegram_bot = TelegramBot(config, input_func=input_func)
    await telegram_bot.run()
