from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    image = models.ImageField(upload_to='users_imges', null=True, blank=True)
    group = models.CharField(max_length=7)