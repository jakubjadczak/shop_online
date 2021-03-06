# Generated by Django 4.0.1 on 2022-03-18 10:26

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_alter_offer_color_alter_offer_condition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=tinymce.models.HTMLField(max_length=4500, verbose_name='Opis'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='short_description',
            field=models.CharField(max_length=200, verbose_name='Krótki opis'),
        ),
    ]
