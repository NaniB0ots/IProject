from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=150, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return f'{self.tag}'


class Student(models.Model):
    lastname = models.CharField(max_length=150, verbose_name='Фамилия')
    firstname = models.CharField(max_length=150, verbose_name='Имя')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', blank=True)

    group = models.CharField(max_length=150, verbose_name='Группа')

    tags = models.ManyToManyField(Tag, verbose_name='Теги (кмпетенции)')

    in_the_project = models.BooleanField(default=False, verbose_name='В проекте')

    class Meta:
        verbose_name = 'Студента'
        verbose_name_plural = 'Студент'

    def __str__(self):
        return f'{self.lastname} {self.firstname}'


class Teacher(models.Model):
    lastname = models.CharField(max_length=150, verbose_name='Фамилия')
    firstname = models.CharField(max_length=150, verbose_name='Имя')
    patronymic = models.CharField(max_length=150, verbose_name='Отчество', blank=True)

    post = models.CharField(max_length=250, verbose_name='Должность')

    tags = models.ManyToManyField(Tag, verbose_name='Теги (кмпетенции)')

    class Meta:
        verbose_name = 'Преподавателя'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return f'{self.lastname} {self.firstname}'


class Project(models.Model):
    title = models.CharField(max_length=300, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    students = models.ManyToManyField(Student, blank=True, verbose_name='Студенты')
    teacher = models.ForeignKey(Teacher, blank=True, null=True,
                                on_delete=models.SET_NULL, verbose_name='Преподаватель')

    tags = models.ManyToManyField(Tag, verbose_name='Теги')

    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return f'{self.title}'
