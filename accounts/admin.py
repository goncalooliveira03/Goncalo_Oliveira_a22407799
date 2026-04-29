from django.contrib import admin
from .models import MagicLinkToken

@admin.register(MagicLinkToken)
class MagicLinkTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'used')