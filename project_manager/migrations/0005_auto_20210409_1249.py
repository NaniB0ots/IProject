# Generated by Django 3.2 on 2021-04-09 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_manager', '0004_auto_20210409_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
