# Generated by Django 5.1.4 on 2024-12-10 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_lesson_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={},
        ),
        migrations.RemoveField(
            model_name='task',
            name='start_time',
        ),
    ]
