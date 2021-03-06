from django.core.management.base import BaseCommand
from tg_bot.tg_bot import bot
from tg_bot import models
from project_manager import models as project_manager_models
from tg_bot import core
from tg_bot.utils import keyboards


class Command(BaseCommand):
    help = 'Рассылка проектов'

    def handle(self, *args, **options):
        print('Запуск расслки...')

        projects = project_manager_models.Project.objects.filter(sent_out=False)

        for project in projects.all():
            students = models.TgUser.objects.filter(student_profile__tags__in=project.tags.all()).distinct()
            for student in students.all():
                try:
                    bot.send_message(chat_id=student.chat_id, text=core.Project.get_project_info_str(project),
                                     parse_mode='html',
                                     reply_markup=keyboards.get_inline_subscribe_for_project_keyboard(project.id))
                except Exception as e:
                    pass

        print('  Расслка закончена')
