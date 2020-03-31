#!/usr/bin/env python3

from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    Filters,
    MessageHandler,
)


from bot.handlers.categories import (
    CategoryHandler,
    CATEGORY_COMMANDS,
    CATEGORY_NAMES,
)
from bot.handlers.transactions import TRANSACTION_NAMES
from bot.handlers.callbacks import (
    DefaultCallbacksHandler,
    CategoryCallbacksHandler,
    TransactionCallbacksHandler,
)
from bot.handlers.commands import DefaultCommandsHandler
from bot.handlers.messages import DefaultMessagesHandler


class Command(BaseCommand):
    help = "Run telegram bot in foreground"

    def _add_command_handlers(self, dispatcher):
        """
        Method add CommandHandlers to dispatcher.
        """

        for command in (
            "help",
            "start",
            "stop",
            "unlink",
            "categories",
            "transactions",
        ):
            print(command)
            dispatcher.add_handler(
                CommandHandler(
                    command, getattr(DefaultCommandsHandler, command)
                )
            )

    def _add_callback_handlers(self, dispatcher):
        """
        Method add CallbackQueryHandlers to dispatcher.
        """

        for callback in CATEGORY_COMMANDS:
            dispatcher.add_handler(
                CallbackQueryHandler(
                    getattr(DefaultCallbacksHandler, callback),
                    pattern=f"^{callback}",
                )
            )

        for callback in CATEGORY_NAMES:
            dispatcher.add_handler(
                CallbackQueryHandler(
                    getattr(CategoryCallbacksHandler, callback),
                    pattern=f"^{callback}$",
                )
            )

        for callback in TRANSACTION_NAMES:
            dispatcher.add_handler(
                CallbackQueryHandler(
                    getattr(TransactionCallbacksHandler, callback),
                    pattern=f"^{callback}$",
                )
            )

    def _add_message_handlers(self, dispatcher):
        dispatcher.add_handler(
            MessageHandler(Filters.text, DefaultMessagesHandler())
        )

    def handle(self, *args, **options):
        import logging

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        updater = Updater(token=settings.BOT_TOKEN, use_context=True,)
        dispatcher = updater.dispatcher

        self._add_command_handlers(dispatcher)
        self._add_callback_handlers(dispatcher)
        self._add_message_handlers(dispatcher)

        updater.start_polling()
