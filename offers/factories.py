import random

import factory
from factory.fuzzy import FuzzyText
from faker import Factory, Faker
from .models import Offer

faker = Factory.create()
fake = Faker('pl_PL')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.Customuser'
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda n: f'user.user{n}@shoponline.com')
    first_name = factory.LazyAttribute(lambda x: fake.name())
    last_name = factory.LazyAttribute(lambda x: fake.last_name())
    city = factory.LazyAttribute(lambda x: fake.city())
    address = factory.LazyAttribute(lambda x: fake.address())
    zip_code = factory.LazyAttribute(lambda x: fake.postcode())
    username = email
    password = 'Shop!@123Hyt'


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'offers.Offer'
        django_get_or_create = ('title',)

    title = factory.LazyAttribute(lambda x: fake.text(random.randint(20, 70)))
    short_description = factory.LazyAttribute(lambda x: fake.text(random.randint(40, 200)))
    description = factory.LazyAttribute(lambda x: fake.text(random.randint(1000, 4500)))
    price = factory.LazyAttribute(lambda x: faker.random.randrange(0, 2000))
    negotiations = factory.LazyAttribute(lambda x: fake.boolean())
    owner = factory.SubFactory(UserFactory)
    titular_photo = factory.django.FileField(filename='piesek.jpg')
    active = factory.LazyAttribute(lambda x: fake.boolean())
    producer = factory.LazyAttribute(lambda x: fake.company())
    color = factory.LazyAttribute(lambda x: fake.color_name())
    weight = factory.LazyAttribute(lambda x: faker.random.randrange(5, 5000, 100))
    condition = factory.LazyAttribute(lambda x: fake.random.randint(1, 3))

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create: return
        if extracted:
            for category in extracted:
                self.categories.add(category)


class PhotoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'offers.Photo'

    photo = factory.django.FileField(filename='ojoj.jpg')
    offer = factory.SubFactory(OfferFactory)


