import six
from typing import List, Optional

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext

from bot.models import TelegramUser


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp)


def get_username(update: Update) -> Optional[TelegramUser]:
    tg_username = update.effective_user.username

    try:
        return TelegramUser.objects.get(tg_username=tg_username).user
    except ObjectDoesNotExist:
        pass
    return None


def get_update(*args: List[object]) -> Optional[Update]:
    return next(filter(lambda x: isinstance(x, Update), args), None)


def get_callback_context(*args: List[object]) -> Optional[CallbackContext]:
    return next(filter(lambda x: isinstance(x, CallbackContext), args), None)
