from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about', views.about),
    path('contact', views.schedule_view, name ='view_contact'),
    path('testpic', views.testpic),
    path('calendar', views.calendar, name = 'view_calendar'),
    path('mainpage', views.mainpage),
    path('contact', views.contact),
    path('deadline', views.deadline, name = 'view_deadline'),
    path('calendar2', views.calendar2, name = 'view_calendar2'),
    path('schedule/', views.schedule_view1, {'offset': 0}, name='schedule'),
    re_path(r'^schedule/(?P<offset>-?\d+)/$', views.schedule_view1, name='schedule_offset'),
    path('schedule/add/', views.add_lesson, name='add_lesson'),
    path('schedule/delete/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
    path('schedule/parse/', views.parse_schedule, name='parse_schedule'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
