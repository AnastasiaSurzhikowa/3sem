from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('about', views.about),
    path('contact', views.schedule_view),
    path('testpic', views.testpic),
    path('calendar', views.calendar),
    path('mainpage', views.mainpage),
    path('contact', views.contact),
    path('deadline', views.deadline),
    path('calendar2', views.calendar2)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
