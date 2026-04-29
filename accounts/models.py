from django.db import models
from django.contrib.auth.models import User
import secrets
from django.utils import timezone
from datetime import timedelta


class MagicLinkToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='magic_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_valid(self):
        expiry = self.created_at + timedelta(minutes=15)
        return not self.used and timezone.now() < expiry

    @classmethod
    def create_for_user(cls, user):
        cls.objects.filter(user=user, used=False).update(used=True)
        token = secrets.token_urlsafe(32)
        return cls.objects.create(user=user, token=token)

    def __str__(self):
        return f"MagicLink para {self.user.username} ({self.created_at})"