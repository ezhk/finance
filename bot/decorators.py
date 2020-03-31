import json

from django.core.exceptions import ObjectDoesNotExist
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from bot.models import TelegramUser, TelegramMessages
from bot.utils import get_username, get_update, get_callback_context


def username_extension(func):
    """
    Decorator validates username link between TG and site
        and also add username value as latest funcion argument.
    """

    def wrapper(*args):
        update = get_update(*args)
        context = get_callback_context(*args)
        if update is None or context is None:
            return None

        username = get_username(update)
        if not username:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You don't link telegram user with site user. "
                + "Try /start command.",
            )
            return None

        return func(*args, username)

    return wrapper


def logger(func):
    """
    Decorator logger store user messages and
        commands into TelegramMessages table.
    """

    def wrapper(*args):
        update = get_update(*args)
        context = get_callback_context(*args)
        if update is None or context is None:
            return None

        try:
            username = TelegramUser.objects.get(
                tg_username=update.effective_user.username
            )
        except ObjectDoesNotExist:
            # on /start action user doesn't exist
            return func(*args)

        message = {}

        try:
            message.update({"message_text": update.effective_message.text})
        except:
            pass

        try:
            message.update({"callback_data": update.callback_query.data})
        except:
            pass

        if message:
            m = TelegramMessages(
                tg_username=username, json_message=json.dumps(message)
            )
            m.save()

        return func(*args)

    return wrapper
