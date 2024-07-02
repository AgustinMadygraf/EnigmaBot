#EnigmaBot/core/telegram_command_handler.py
from telegram import Update, ForceReply
from telegram.ext import CallbackContext
from logs.config_logger import LoggerConfigurator

logger = LoggerConfigurator().get_logger()

class TelegramCommandHandler:
    """Clase para manejar los comandos de Telegram."""

    def start(self, update: Update, context: CallbackContext) -> None:
        """
        Maneja el comando /start.

        :param update: El objeto update que contiene el mensaje del usuario.
        :param context: El objeto context que contiene información sobre el chat.
        """
        user = update.effective_user
        logger.debug("Comando /start recibido de usuario: %s", user.mention_markdown_v2())
        
        update.message.reply_markdown_v2(
            fr'Hola {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )
