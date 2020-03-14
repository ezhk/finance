from abc import ABCMeta, abstractmethod

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.utils import timezone

from bot.decorators import username_extension
from main.models import (
    IncomeTransaction,
    ExpenseTransaction,
    IncomeSource,
    Asset,
    ExpenseCategory,
)


TRANSACTION_NAMES = ("incoming", "outgoing")


class TransactionHandler(metaclass=ABCMeta):
    MODEL = None
    BUTTONS = (
        InlineKeyboardButton(text="show", callback_data="show"),
        InlineKeyboardButton(text="create", callback_data="create"),
        InlineKeyboardButton(text="delete", callback_data="delete_menu"),
    )
    CREATE_DIALOG = ({"text": None, "reply_markup": None, "next": None},)

    @staticmethod
    def _create_dialog(username):
        pass

    @classmethod
    def _dialog_generator(cls, username):
        for dialog_params in cls._create_dialog(username):
            yield dialog_params

    @classmethod
    def _start_dialog(cls, update, context):
        try:
            dialog_params = next(context.user_data["dialog"])
            context.user_data["next"] = dialog_params.get("next")

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=dialog_params.get("text"),
                reply_markup=dialog_params.get("reply_markup", None),
            )
        except StopIteration:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Error: empty dialog"
            )
        except Exception as err:
            print(err)

    @classmethod
    @abstractmethod
    def select_item(cls, update, context):
        try:
            _, pk = update.callback_query.data.split(":", 1)
            context.user_data.update({context.user_data["next"]: pk})

            dialog_params = next(context.user_data["dialog"])
            context.user_data["next"] = dialog_params["next"]

            message = dialog_params["text"]
            reply_markup = dialog_params.get("reply_markup", None)
        except Exception as err:
            return context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Error while create transaction, {err}",
            )

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup,
        )

    @staticmethod
    def _get_model_by_name(classname):
        if classname == "asset":
            return Asset
        elif classname == "income":
            return IncomeSource
        elif classname == "expense":
            return ExpenseCategory
        return None

    @classmethod
    @username_extension
    @abstractmethod
    def process_dialog(cls, update, context, username):
        model_data = {}
        for field, value in context.user_data.items():
            try:
                cls.MODEL._meta.get_field(field)

                field_model = cls._get_model_by_name(field)
                if field_model is not None:
                    value = field_model.objects.get(pk=value, user=username)

                model_data[field] = value
            except:
                pass

        new_category = cls.MODEL(**model_data)
        try:
            new_category.save()
        except Exception as err:
            return f"Error: {err}, try again."

        return "Transaction has created"

    @classmethod
    @username_extension
    @abstractmethod
    def show(cls, update, context, username):
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="\n".join(
                [
                    f"- {record} "
                    for record in cls.MODEL.objects.filter(
                        asset__user=username,
                        created_at__year=timezone.now().year,
                        created_at__month=timezone.now().month,
                    ).order_by("created_at")
                ]
            )
            or "Empty list for this month",
        )

    @classmethod
    @username_extension
    @abstractmethod
    def create(cls, update, context, username):
        context.user_data["dialog"] = cls._dialog_generator(username)
        cls._start_dialog(update, context)

    @classmethod
    @username_extension
    @abstractmethod
    def delete_menu(cls, update, context, username):
        """Delete category by ID."""
        markup = InlineKeyboardMarkup([])
        for record in cls.MODEL.objects.filter(
            asset__user=username,
            created_at__year=timezone.now().year,
            created_at__month=timezone.now().month,
        ).order_by("created_at"):
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
            text="Delete transaction",
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

        status = cls.MODEL.objects.filter(asset__user=username, pk=pk).delete()
        return context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Delete transaction status: {status}",
        )


class IncomingHandler(TransactionHandler):
    MODEL = IncomeTransaction

    @staticmethod
    def _create_dialog(username):
        return (
            {
                "text": "Choose income category",
                "reply_markup": InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{category}",
                                callback_data=f"select_item:{category.pk}",
                            )
                        ]
                        for category in IncomeSource.objects.filter(
                            user=username
                        )
                    ]
                ),
                "next": "income",
            },
            {
                "text": "Choose Asset category",
                "reply_markup": InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{category}",
                                callback_data=f"select_item:{category.pk}",
                            )
                        ]
                        for category in Asset.objects.filter(user=username)
                    ]
                ),
                "next": "asset",
            },
            {"text": "Input tranmsaction amount", "next": "amount",},
        )


class OutgoingHandler(TransactionHandler):
    MODEL = ExpenseTransaction

    @staticmethod
    def _create_dialog(username):
        return (
            {
                "text": "Choose asset category",
                "reply_markup": InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{category}",
                                callback_data=f"select_item:{category.pk}",
                            )
                        ]
                        for category in Asset.objects.filter(user=username)
                    ]
                ),
                "next": "asset",
            },
            {
                "text": "Choose expense category",
                "reply_markup": InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=f"{category}",
                                callback_data=f"select_item:{category.pk}",
                            )
                        ]
                        for category in ExpenseCategory.objects.filter(
                            user=username
                        )
                    ]
                ),
                "next": "expense",
            },
            {
                "text": "Input tranmsaction amount",
                "reply_markup": None,
                "next": "amount",
            },
        )
