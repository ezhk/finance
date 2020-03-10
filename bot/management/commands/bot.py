#!/usr/bin/env python3

from django.conf import settings
from django.core.management.base import BaseCommand
from telegram.ext import Updater, CommandHandler

from bot.utils import BotHandlers


class Command(BaseCommand):
    help = "Run telegram bot in foreground"

    def handle(self, *args, **options):
        updater = Updater(token=settings.BOT_TOKEN, use_context=True,)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler("start", BotHandlers.start))
        dispatcher.add_handler(CommandHandler("stop", BotHandlers.stop))
        dispatcher.add_handler(CommandHandler("unlink", BotHandlers.unlink))

        dispatcher.add_handler(CommandHandler("incomes", BotHandlers.incomes))
        dispatcher.add_handler(CommandHandler("assets", BotHandlers.assets))
        dispatcher.add_handler(
            CommandHandler("expenses", BotHandlers.expenses)
        )
        dispatcher.add_handler(
            CommandHandler("transaction", BotHandlers.transaction)
        )

        updater.start_polling()

        # bot = telegram.Bot(
        #     token=settings.BOT_TOKEN
        # )
        # print(bot.get_me())
        # {'id': 1013240804, 'first_name': 'finance-pyexec-test', 'is_bot': True, 'username': 'FinancePyexecTestBot'}
