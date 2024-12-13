from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Lesson(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lessons",
        default=1
    )
    DAY_CHOICES = [
        ('ПН', 'Понедельник'),
        ('ВТ', 'Вторник'),
        ('СР', 'Среда'),
        ('ЧТ', 'Четверг'),
        ('ПТ', 'Пятница'),
        ('СБ', 'Суббота'),
        ('ВС', 'Воскресенье'),
    ]

    TYPE_CHOICES = [
        ('Л', 'Лекция'),
        ('ПР', 'Практическое занятие'),
        ('ЛР', 'Лабораторное занятие'),
        ('КП', 'Курсовой проект'),
        ('КР', 'Курсовая работа'),
    ]

    # Изменение поля на CharField для поддержания "оба" значения
    week_parity = models.CharField(
        max_length=2,
        choices=[('Ч', 'Чётная'), ('Н', 'Нечётная'), ('Б', 'Обе')],
        default='Ч',
    )  # 'Ч' для чётной, 'Н' для нечетной, 'Б' для обеих недель

    day = models.CharField(max_length=2, choices=DAY_CHOICES)
    subject = models.CharField(max_length=255)
    room = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lesson_type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.subject} ({self.lesson_type}) - {self.day}"
    
class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks",
        default=1
    )
    date = models.DateField(default=now)  # Указываем дату, которая будет назначаться при добавлении
    subject = models.CharField(max_length=255)
    descriptions = models.CharField(max_length=511)

    def __str__(self):
        return f"{self.subject} - {self.date}"
