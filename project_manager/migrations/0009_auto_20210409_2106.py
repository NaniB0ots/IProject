# Generated by Django 3.2 on 2021-04-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0008_project_sent_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='connection',
            field=models.CharField(blank=True, default='Связь (Номер телефона, email  т.п.)', max_length=150),
        ),
        migrations.AddField(
            model_name='teacher',
            name='connection',
            field=models.CharField(blank=True, default='Связь (Номер телефона, email  т.п.)', max_length=150),
        ),
    ]