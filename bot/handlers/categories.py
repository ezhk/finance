from abc import ABCMeta, abstractmethod

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from bot.decorators import username_extension
from main.models import IncomeSource, Asset, ExpenseCategory


CATEGORY_NAMES = ("incomes", "assets", "expenses")
CATEGORY_COMMANDS = ("show", "create", "delete_menu", "delete_item")


class CategoryHandler(metaclass=ABCMeta):
    MODEL = None

    BUTTONS = (
        InlineKeyboardButton(text="show", callback_data="show"),
        InlineKeyboardButton(text="create", callback_data="create"),
        InlineKeyboardButton(text="delete", callback_data="delete_menu"),
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
    @username_extension
    @abstractmethod
    def process_dialog(cls, update, context, username):
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
    @username_extension
    @abstractmethod
    def show(cls, update, context, username):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="\n".join(
                [
                    f"- {record} "
                    for record in cls.MODEL.objects.filter(user=username)
                ]
            ),
        )

    @classmethod
    @abstractmethod
    def create(cls, update, context):
        """Create category object."""
        context.user_data["dialog"] = cls._dialog()
        cls._start_dialog(update, context)

    @classmethod
    @username_extension
    @abstractmethod
    def delete_menu(cls, update, context, username):
        """Delete category by ID."""
        markup = InlineKeyboardMarkup([])
        for record in cls.MODEL.objects.filter(user=username):
            markup.inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text=f"{record}",
                        callback_data=f"delete_item:{record.pk}",
                    )
                ]
            )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Delete record",
            reply_markup=markup,
        )

    @classmethod
    @username_extension
    @abstractmethod
    def delete_item(cls, update, context, username):
        try:
            _, pk = update.callback_query.data.split(":", 1)
        except ValueError as err:
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Error: wrong delete action {err}",
            )

        status = cls.MODEL.objects.filter(user=username, pk=pk).delete()
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Delete category status: {status}",
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
