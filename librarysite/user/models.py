from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import ModelMixin



class User(ModelMixin, AbstractUser):
    is_admin = models.BooleanField(default=False)
    username = models.CharField('Username', max_length=20, unique=True)
    email = models.EmailField('Email', unique=True)
    password_need_reset = models.BooleanField(default=False)


    def __str__(self):
        return self.username
