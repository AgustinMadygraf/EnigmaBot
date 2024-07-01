#EnigmaBot/core/telegram_command_handler.py
from telegram import Update, ForceReply
from telegram.ext import CallbackContext

class TelegramCommandHandler:
    """Class to handle Telegram commands."""

    def start(self, update: Update, context: CallbackContext) -> None:
        """
        Handle the /start command.

        :param update: The update object containing the user's message.
        :param context: The context object containing information about the chat.
        """
        user = update.effective_user
        update.message.reply_markdown_v2(
            fr'Hola {user.mention_markdown_v2()}\!',
            reply_markup=ForceReply(selective=True),
        )
