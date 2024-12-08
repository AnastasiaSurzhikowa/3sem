from django.db import models

class Lesson(models.Model):
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

    day = models.CharField(max_length=2, choices=DAY_CHOICES)
    week_parity = models.BooleanField(default=True)  # True = четная неделя, False = нечетная
    subject = models.CharField(max_length=255)
    room = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lesson_type = models.CharField(max_length=2, choices=TYPE_CHOICES)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.subject} ({self.lesson_type}) - {self.day}"
