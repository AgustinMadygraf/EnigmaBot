#EnigmaBot/core/telegram_bot.py
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from core.chatbot import ChatBot
import os

class TelegramBot:
    def __init__(self, config, input_func=input):
        self.config = config
        self.chatbot = ChatBot(config, input_func=input_func)
        self.token = os.getenv("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("No TELEGRAM_TOKEN found in environment variables")

    def start(self, update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        update.message.reply_markdown_v2(
            fr'Hola {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )

    def echo(self, update: Update, context: CallbackContext) -> None:
        user_message = update.message.text
        self.chatbot.procesar_mensaje("telegram_user", user_message)
        response = self.chatbot.generar_respuesta("telegram_user")
        update.message.reply_text(response)

    def run(self):
        application = Application.builder().token(self.token).build()

        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo))

        application.run_polling(stop_signals=None)

async def iniciar_chat_telegram(config, input_func, model_class):
    telegram_bot = TelegramBot(config, input_func=input_func)
    telegram_bot.run()
