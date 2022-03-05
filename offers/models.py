from django.db import models
import django.utils.timezone as t
from tinymce import models as tiny_model
from sorl.thumbnail import ImageField


def upload_to(instance, filename):
    return f'offers{instance.pk}/{filename}'


class Category(models.Model):
    name = models.CharField(verbose_name='Nazwa kategorii')


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
    description = tiny_model.HTMLField(max_length=500, verbose_name='Opis'),
    price = models.FloatField(verbose_name='Cena'),
    negotiations = models.BooleanField(verbose_name='Możliwość negocjacji'),
    data = models.DateField(verbose_name='Data', default=t.now()),
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='offer', verbose_name='Sprzedawca'),
    titular_photo = ImageField(upload_to=upload_to, verbose_name='Zdjęcie tytułowe')
    active = models.BooleanField(default=True, verbose_name='Aktywna'),
    categories = models.ManyToManyField(Category, related_name='categories'),
    producer = models.CharField(max_length=100, verbose_name='Producent', blank=True, null=True),
    color = models.CharField(max_length=50, verbose_name='Kolor', blank=True, null=True),
    weight = models.FloatField(verbose_name='Waga', blank=True, null=True)
    condition = models.CharField(max_length=10, choices=STATUS, default=NEW)


class Photo(models.Model):
    photo = ImageField(verbose_name='Zdjęcie')
    has_offer = models.BooleanField(default=True, verbose_name='Powiązane z ofertą')
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='photos', verbose_name='Oferta')
