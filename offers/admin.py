from django.contrib import admin
from .models import Offer, Photo, Category


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'price', 'date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Photo)
class PhtoAdmin(admin.ModelAdmin):
    list_display = ['offer']