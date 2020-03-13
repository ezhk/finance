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
from bot.handlers.callbacks import (
    DefaultCallbacksHandler,
    CategoryCallbacksHandler,
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

    def _add_message_handlers(self, dispatcher):
        dispatcher.add_handler(
            MessageHandler(Filters.text, DefaultMessagesHandler())
        )

    def handle(self, *args, **options):
        updater = Updater(token=settings.BOT_TOKEN, use_context=True,)
        dispatcher = updater.dispatcher

        self._add_command_handlers(dispatcher)
        self._add_callback_handlers(dispatcher)
        self._add_message_handlers(dispatcher)

        updater.start_polling()

        # bot = telegram.Bot(
        #     token=settings.BOT_TOKEN
        # )
        # print(bot.get_me())
        # {'id': 1013240804, 'first_name': 'finance-pyexec-test', 'is_bot': True, 'username': 'FinancePyexecTestBot'}
