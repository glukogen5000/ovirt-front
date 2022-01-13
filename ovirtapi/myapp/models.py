from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


class User_list(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=250)
    password = models.CharField(verbose_name='Пароль', max_length=250, null=True, blank=True)
    email = models.CharField(verbose_name='Email', max_length=250, null=True, blank=True)
    account = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    balanse = models.IntegerField(verbose_name='Баланс', blank=True, null=True)
    def __str__(self):
        return self.name
