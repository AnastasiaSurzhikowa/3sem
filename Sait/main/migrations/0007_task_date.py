# Generated by Django 5.1.4 on 2024-12-11 01:44

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
