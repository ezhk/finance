from django.core.exceptions import ObjectDoesNotExist
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from bot.models import TelegramUser


def username_extension(func):
    """
    Decorator validates username link between TG and site
      and also add username value as latest funcion argument.
    """

    def _get_username(update):
        tg_username = update.effective_user.username

        try:
            return TelegramUser.objects.get(tg_username=tg_username).user
        except ObjectDoesNotExist:
            pass
        return None

    def wrapper(*args):
        try:
            update = next(filter(lambda x: isinstance(x, Update), args))
            context = next(
                filter(lambda x: isinstance(x, CallbackContext), args)
            )
        except StopIteration:
            # objects not found
            return None

        username = _get_username(update)
        if not username:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You don't link telegram user with sire user. "
                + "Try /start command.",
            )
            return None

        return func(*args, username)

    return wrapper
