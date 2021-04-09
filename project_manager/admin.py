from django.contrib import admin
from project_manager import models


@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('lastname', 'firstname', 'patronymic', 'group', 'in_the_project')
    search_fields = ('lastname', 'firstname', 'patronymic', 'group',)
    list_filter = ('group', 'in_the_project')
    ordering = ['lastname', 'firstname']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass
