from django.conf import settings
from django.db import models


class TelegramUser(models.Model):
    """
    https://core.telegram.org/method/account.checkUsername
    username accepted characters:
      A-z (case-insensitive), 0-9 and underscores.
      Length: 5-32 characters.

    By default user not defined.
    User need to follow link for creation relatoionship
        between TG user and site's username.
    """

    tg_username = models.CharField(
        verbose_name="Telegram username",
        max_length=32,
        blank=False,
        unique=True,
        db_index=True,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )

    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

    def link(self, user):
        """
        Create link between TG and site accounts.
        """
        self.user = user
        self.save()

    def unlink(self):
        self.user = None
        self.save()


class TelegramMessages(models.Model):
    tg_username = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    json_message = models.CharField(
        verbose_name="User message presented as JSON",
        max_length=2048,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
