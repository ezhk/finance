from urllib.parse import urljoin

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ParseMode,
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
    """
    Class describe commands in bot calls.
        /start and /stop are base commands.
        /help sets keyboard with all possible commands.
    """

    @staticmethod
    def start(update, context):
        """
        /start command checks links between current
            TG user and sire user, and if user doesn't
            create link — show specially link to site.
        """

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
        url = urljoin(
            settings.SITE_URL,
            reverse(
                "bot:link-account",
                kwargs={
                    "username": tg_username,
                    "chat": update.effective_chat.id,
                    "token": token,
                },
            ),
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Hello, @{tg_username}. "
            + "You need to link your telegram account and site account: "
            + f"sign in on the site and follow the link {url}",
        )

    @staticmethod
    def stop(update, context):
        """
        Make user inactive.
        """

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
        """
        Remove link to site username for current TG user.
        """

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
            text="*Categories*",
            reply_markup=InlineKeyboardMarkup([buttons]),
            parse_mode=ParseMode.MARKDOWN,
        )

    @classmethod
    def incomes(cls, update, context):
        context.user_data["handler"] = IncomeHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Categories* > *Incomes*",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    @classmethod
    def assets(cls, update, context):
        context.user_data["handler"] = AssetHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Categories* > *Assets*",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    @classmethod
    def expenses(cls, update, context):
        context.user_data["handler"] = ExpenseHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Categories* > *Expenses*",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    @staticmethod
    def transactions(update, context):
        """
        Meta method for choosing selected trancation type:
          incomes (incoming method) or expenses (outgoing method)
          and call their methods.
        """

        buttons = [
            InlineKeyboardButton(
                text=category.capitalize(), callback_data=category
            )
            for category in TRANSACTION_NAMES
        ]

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Transactions*",
            reply_markup=InlineKeyboardMarkup([buttons]),
            parse_mode=ParseMode.MARKDOWN,
        )

    @classmethod
    def incoming(cls, update, context):
        context.user_data["handler"] = IncomingHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Transactions* > *Incoming*",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    @classmethod
    def outgoing(cls, update, context):
        context.user_data["handler"] = OutgoingHandler

        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="*Transactions* > *Outgoing*",
            reply_markup=InlineKeyboardMarkup(
                [context.user_data["handler"].BUTTONS]
            ),
            parse_mode=ParseMode.MARKDOWN,
        )

    @staticmethod
    def help(update, context):
        """
        Show full supported keuboard map.
        """

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
