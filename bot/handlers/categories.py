from abc import ABCMeta, abstractmethod

from django.core.exceptions import ObjectDoesNotExist
from telegram import InlineKeyboardButton

from bot.models import TelegramUser
from main.models import IncomeSource, Asset, ExpenseCategory


class CategoryHandler(metaclass=ABCMeta):
    MODEL = None
    BUTTONS = (
        InlineKeyboardButton(text="show", callback_data="show"),
        InlineKeyboardButton(text="create", callback_data="create"),
        InlineKeyboardButton(text="delete", callback_data="delete"),
    )
    CREATE_DIALOG = ((None, None),)

    @classmethod
    def _dialog(cls):
        for message, next_value in cls.CREATE_DIALOG:
            yield message, next_value

    @classmethod
    def _start_dialog(cls, update, context):
        try:
            message, next_value = next(context.user_data["dialog"])
            context.user_data["next"] = next_value

            context.bot.send_message(
                chat_id=update.effective_chat.id, text=message
            )
        except StopIteration:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Error: empty dialog"
            )

    @classmethod
    def _get_username(cls, update):
        tg_username = update.effective_user.username

        try:
            return TelegramUser.objects.get(tg_username=tg_username).user
        except ObjectDoesNotExist:
            pass
        return None

    @classmethod
    def process_dialog(cls, update, context):
        username = cls._get_username(update)
        if not username:
            return (
                "You don't link telegram user with sire user. "
                + "Try /start command."
            )

        model_data = {}
        for field, value in context.user_data.items():
            try:
                cls.MODEL._meta.get_field(field)
                model_data[field] = value
            except:
                pass

        new_category = cls.MODEL(user=username, **model_data)
        try:
            new_category.save()
        except Exception as err:
            return f"Error: {err}, try again."

        return "Category has created"

    @classmethod
    def show(cls, update, context):
        username = cls._get_username(update)
        if not username:
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You don't link telegram user with sire user. "
                + "Try /start command.",
            )

        for record in cls.MODEL.objects.filter(user=username):
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=str(record)
            )

    @classmethod
    def create(cls, update, context):
        """Create category object."""
        context.user_data["dialog"] = cls._dialog()
        cls._start_dialog(update, context)

    @classmethod
    @abstractmethod
    def delete(cls, update, context):
        """Delete category by ID."""
        username = cls._get_username(update)
        if not username:
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="You don't link telegram user with sire user. "
                + "Try /start command.",
            )


class IncomeHandler(CategoryHandler):
    MODEL = IncomeSource
    CREATE_DIALOG = (("Input category name", "description"),)


class AssetHandler(CategoryHandler):
    MODEL = Asset
    CREATE_DIALOG = (
        ("Input asset name", "description"),
        ("Input start balance", "balance"),
        (
            "Input asset type "
            + f"({Asset.CASH} = cash, "
            + f"{Asset.BANK_CARD} = bank card, "
            + f"{Asset.CREDIT_CARD} = credit card)",
            "type",
        ),
    )


class ExpenseHandler(CategoryHandler):
    MODEL = ExpenseCategory
    CREATE_DIALOG = (
        ("Input expense name", "description"),
        ("Input monthly limit", "monthly_limit"),
    )
