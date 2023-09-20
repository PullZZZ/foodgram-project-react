# Generated by Django 4.2.4 on 2023-09-19 16:50

from django.db import migrations, models
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_favorite_recipes_allready_in_favorite_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, validators=[recipes.validators.RecipeNameValidator], verbose_name='Название'),
        ),
    ]
