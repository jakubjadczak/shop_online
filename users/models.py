from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='email')
    first_name = models.CharField(max_length=80, verbose_name='imię')
    last_name = models.CharField(max_length=100, verbose_name='nazwisko')
    city = models.CharField(max_length=100, verbose_name='miasto')
    address = models.CharField(max_length=200, verbose_name='adres')
    zip_code = models.CharField(max_length=7, verbose_name='kod pocztowy')
    reset_code = models.CharField(max_length=6, verbose_name='kod', null=True, blank=True)