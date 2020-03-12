from abc import ABCMeta, abstractmethod

from telegram import InlineKeyboardButton


class TransactionHandler(metaclass=ABCMeta):
    MODEL = None
    BUTTONS = (
        InlineKeyboardButton(text="show", callback_data="show"),
        InlineKeyboardButton(text="create", callback_data="create"),
        InlineKeyboardButton(text="delete", callback_data="delete"),
    )

    @classmethod
    @abstractmethod
    def show(cls, update, context):
        pass

    @classmethod
    @abstractmethod
    def create(cls, update, context):
        pass

    @classmethod
    @abstractmethod
    def delete(cls, update, context):
        pass
