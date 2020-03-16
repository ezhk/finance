from django.urls import path

from bot.views import LinkAccount

app_name = "bot"
urlpatterns = [
    path(
        "link/<slug:username>/<int:chat>/<slug:token>/",
        LinkAccount.as_view(),
        name="link-account",
    ),
]
