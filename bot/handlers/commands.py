from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from bot.models import TelegramUser
from bot.utils import TokenGenerator

from bot.handlers.categories import (
    IncomeHandler,
    AssetHandler,
    ExpenseHandler,
    CATEGORY_NAMES,
)
from bot.handlers.transactions import (
    IncomingHandler,
    OutgoingHandler,
    TRANSACTION_NAMES,
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
    def categories(cls, update, context):
        """
        Meta method for choosing selected category:
          assets, incomes or expenses and call their method.
        """

        buttons = [
            InlineKeyboardButton(
                text=category.capitalize(), callback_data=category
            )
            for category in CATEGORY_NAMES
        ]

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Categories",
            reply_markup=InlineKeyboardMarkup([buttons]),
        )

    @classmethod
    def incomes(cls, update, context):
        context.user_data["handler"] = IncomeHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Categories > Incomes",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @classmethod
    def assets(cls, update, context):
        context.user_data["handler"] = AssetHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Categories > Assets",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @classmethod
    def expenses(cls, update, context):
        context.user_data["handler"] = ExpenseHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Categories > Expenses",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @staticmethod
    def transactions(update, context):
        """
        Meta method for choosing selected trancation type:
          incomes or expenses and call their method.
        """

        buttons = [
            InlineKeyboardButton(
                text=category.capitalize(), callback_data=category
            )
            for category in TRANSACTION_NAMES
        ]

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Transactions",
            reply_markup=InlineKeyboardMarkup([buttons]),
        )

    @classmethod
    def incoming(cls, update, context):
        context.user_data["handler"] = IncomingHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Transactions > Incoming",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @classmethod
    def outgoing(cls, update, context):
        context.user_data["handler"] = OutgoingHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Transactions > Outgoing",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
        )

    @staticmethod
    def help(update, context):
        buttons = [
            ["/categories", "/transactions"],
            ["/start", "/stop"],
            ["/unlink", "/help"],
        ]

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Choose your next keyboard action",
            reply_markup=ReplyKeyboardMarkup(
                buttons, resize_keyboard=False, one_time_keyboard=True
            ),
        )
