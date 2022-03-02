from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'email']
    filter_horizontal = ('groups', 'user_permissions')
