import random
import string
from django.db import models
from django.utils.text import slugify
from tinymce import models as tiny_model
from sorl.thumbnail import ImageField


def upload_to(instance, filename):
    return f'offers/{instance.slug}_{filename}'


def upload_to_photos(instance, filename):
    return f'photos/{instance.offer.slug}_{filename}'


def get_random_text():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(3))


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nazwa kategorii')

    def __str__(self):
        return self.name


class Offer(models.Model):

    class Condition(models.IntegerChoices):
        NEW = 1, 'Nowy'
        USED = 2, 'Używany'
        DAMAGED = 3, 'Uszkodzony'

    title = models.CharField(max_length=70, verbose_name='Tytuł')
    short_description = models.CharField(max_length=200, verbose_name='Krótki opis')
    description = tiny_model.HTMLField(max_length=4500, verbose_name='Opis')
    price = models.FloatField(verbose_name='Cena')
    negotiations = models.BooleanField(verbose_name='Możliwość negocjacji')
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='offer', verbose_name='Sprzedawca')
    titular_photo = ImageField(upload_to=upload_to, verbose_name='Zdjęcie tytułowe')
    active = models.BooleanField(default=True, verbose_name='Aktywna')
    categories = models.ForeignKey(Category, related_name='categories', on_delete=models.CASCADE)
    producer = models.CharField(max_length=200, verbose_name='Producent', blank=True, null=True)
    color = models.CharField(max_length=100, verbose_name='Kolor', blank=True, null=True)
    weight = models.FloatField(verbose_name='Waga', blank=True, null=True)
    condition = models.PositiveSmallIntegerField(default=Condition.NEW, choices=Condition.choices)
    date = models.DateField(verbose_name='Data', auto_now=True)
    bought_date = models.DateField(verbose_name='Data zakupu', blank=True, null=True)
    slug = models.SlugField(verbose_name='Slug', default='slug')

    def save(self, *args, **kwargs):
        slug = slugify(self.title)
        slugs = self.__class__.objects.filter(slug=slug).values_list('slug', flat=True)
        if slugs:
            while True:
                if slug in slugs:
                    slug += get_random_text()
                else:
                    break
        self.slug = slug
        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return self.slug


class Photo(models.Model):
    photo = ImageField(verbose_name='Zdjęcie', upload_to=upload_to_photos)
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE, related_name='photos', verbose_name='Oferta')


class Bought(models.Model):
    buyer = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='bought_buyer', verbose_name='Kupujący')
    seller = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='bought_seller', verbose_name='Sprzedawca')
    offer = models.ForeignKey('offers.Offer', on_delete=models.CASCADE, related_name='bought_offer', verbose_name='offer')
    date = models.DateField(auto_now=True, verbose_name='Data')