from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.views import View

import telegram

from bot.models import TelegramUser
from bot.utils import TokenGenerator


class LinkAccount(View):
    def get(self, request, *args, **kwargs):
        # validate request url params
        try:
            username = kwargs["username"]
            chat = kwargs["chat"]
            token = kwargs["token"]
        except KeyError:
            return HttpResponseBadRequest(
                "Username, chat id or token weren't defined"
            )

        # check user and permissions
        try:
            user = TelegramUser.objects.get(tg_username=username)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Username doesn't exist")
        if not TokenGenerator().check_token(user, token):
            HttpResponseForbidden("Forbidden")

        # linking username
        user.link(request.user)
        user.activate()

        bot = telegram.Bot(token=settings.BOT_TOKEN)
        bot.send_message(
            chat_id=chat,
            text=f"Your account @{username} "
            + f"has linked with {request.user.username}.",
        )
        return HttpResponseRedirect("/")

