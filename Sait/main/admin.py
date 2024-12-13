from django.contrib import admin
from .models import Lesson, Task, Event

admin.site.register(Lesson)
admin.site.register(Task)
admin.site.register(Event)