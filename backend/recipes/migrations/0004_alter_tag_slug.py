# Generated by Django 4.2.4 on 2023-09-22 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_remove_ingredient_unique_ingredient_and_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='Slug категории'),
        ),
    ]
