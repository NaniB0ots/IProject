# Generated by Django 3.2 on 2021-04-09 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0009_auto_20210409_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='connection',
            field=models.CharField(blank=True, max_length=150, verbose_name='Связь (Номер телефона, email  т.п.)'),
        ),
    ]
