from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index),
    path('signin', views.signin, name = 'signin'),
    path('', include('main.urls')),
    path('profile', views.profile, name = 'view_profile'),
    path('logout/', views.logout, name = 'logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)