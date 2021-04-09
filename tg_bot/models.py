from django.db import models
from project_manager import models as project_manager_models


class TgUser(models.Model):
    username = models.CharField(max_length=90)
    chat_id = models.IntegerField()
    student_profile = models.OneToOneField(project_manager_models.Student, on_delete=models.CASCADE)

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания аккаунта')

    class Meta:
        verbose_name = 'Телеграм пользователя'
        verbose_name_plural = 'Телеграм пользователь'

    def __str__(self):
        return f'{self.username}'
