from django.db import models

class users(models.Model):
    username = models.CharField('Username', max_length=20)
    email = models.EmailField('Email')
    password = models.CharField('Password', max_length=128)


def __str__(self):
    return self.title