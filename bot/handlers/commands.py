from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from telegram import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from bot.models import TelegramUser
from bot.utils import TokenGenerator

from bot.handlers.categories import (
    IncomeHandler,
    AssetHandler,
    ExpenseHandler,
)


class DefaultCommandsHandler:
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

    @classmethod
    def incomes(cls, update, context):
        context.user_data["handler"] = IncomeHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Incomes",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @classmethod
    def assets(cls, update, context):
        context.user_data["handler"] = AssetHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Assets",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @classmethod
    def expenses(cls, update, context):
        context.user_data["handler"] = ExpenseHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Expenses",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @staticmethod
    def transaction(update, context):
        pass

    @staticmethod
    def help(update, context):
        buttons = [
            ["/incomes", "/assets"],
            ["/expenses", "/transaction"],
            ["/start", "/stop"],
            ["/unlink"],
        ]

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Actions",
            reply_markup=ReplyKeyboardMarkup(
                buttons, resize_keyboard=False, one_time_keyboard=True
            ),
        )
