from django.contrib import admin
from tg_bot import models


@admin.register(models.TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'chat_id', 'student_profile',)
    search_fields = ('username', 'chat_id',)
    ordering = ['-creation_date', ]
