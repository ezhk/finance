import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from bot.models import TelegramUser


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp)


class BotHandlers:
    """
    Class with static methods for telegram bot handlers.
    """

    @staticmethod
    def start(update, context):
        tg_username = update.effective_user.username
        obj, _ = TelegramUser.objects.select_related().get_or_create(
            tg_username=tg_username
        )

        if obj.user:
            obj.activate()
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Welcome back, @{tg_username}. "
                + f"You already linked as {obj.user.username}.",
            )

        token = TokenGenerator().make_token(obj)
        url = reverse(
            "bot:link-account",
            kwargs={
                "username": tg_username,
                "chat": update.effective_chat.id,
                "token": token,
            },
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Hello, @{tg_username}. "
            + "You need to link your telegram account and site account: "
            + f"sign in on the site and follow the link {url}",
        )

    @staticmethod
    def stop(update, context):
        tg_username = update.effective_user.username

        try:
            TelegramUser.objects.get(tg_username=tg_username).deactivate()
        except ObjectDoesNotExist:
            pass

        return context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"See you, @{tg_username}.",
        )

    @staticmethod
    def unlink(update, context):
        tg_username = update.effective_user.username

        try:
            TelegramUser.objects.get(tg_username=tg_username).unlink()
        except ObjectDoesNotExist:
            pass

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Account @{tg_username} unlinked.",
        )

    @staticmethod
    def incomes(update, context):
        pass

    @staticmethod
    def assets(update, context):
        pass

    @staticmethod
    def expenses(update, context):
        pass

    @staticmethod
    def transaction(update, context):
        pass
