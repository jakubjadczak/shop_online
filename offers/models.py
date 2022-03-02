from django.db import models
import django.utils.timezone as t


class Category(models.Model):
    name = models.CharField(verbose_name='Nazwa kategorii')


class Photo(models.Model):
    photo = models.ImageField(verbose_name='Zdjęcie')


class Offer(models.Model):
    NEW = 'new'
    USED = 'used'
    DAMAGED = 'damaged'

    STATUS = (
        (NEW, 'Nowy'),
        (USED, 'Używany'),
        (DAMAGED, 'Uszkodzony')
    )

    title = models.CharField(max_length=100, verbose_name='Tytuł'),
    short_description = models.CharField(max_length=150, verbose_name='Krótki opis'),
    description = models.CharField(max_length=500, verbose_name='Opis'),
    price = models.FloatField(verbose_name='Cena'),
    negotiations = models.BooleanField(verbose_name='Możliwość negocjacji'),
    data = models.DateField(verbose_name='Data', default=t.now()),
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='offer', verbose_name='Sprzedawca'),
    titular_photo = models.ImageField(verbose_name='Zdjęcie tytułowe')
    photos = models.ManyToManyField(Photo, on_delete=models.CASCADE, verbose_name='Zdjęcia'),
    active = models.BooleanField(default=True, verbose_name='Aktywna'),
    categories = models.ManyToManyField(Category, related_name='categories'),
    producer = models.CharField(max_length=100, verbose_name='Producent', blank=True, null=True),
    color = models.CharField(max_length=50, verbose_name='Kolor', blank=True, null=True),
    weight = models.FloatField(verbose_name='Waga', blank=True, null=True)
    condition = models.CharField(max_length=10, choices=STATUS, default=NEW)
