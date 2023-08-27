from colorfield.fields import ColorField
from django.db import models
from foodgram.settings import MODEL_NAME_MAX_LEN
from users.models import User


class Recipe (models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=MODEL_NAME_MAX_LEN,
        db_index=True,
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='recipes/images/'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления (в минутах)'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('name', )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name='Количество'
    )


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MODEL_NAME_MAX_LEN,
        db_index=True,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=MODEL_NAME_MAX_LEN
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MODEL_NAME_MAX_LEN,
        db_index=True,
    )
    color = ColorField(default='#FF0000')
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=MODEL_NAME_MAX_LEN,
        unique=True,
        null=True
    )

    def __str__(self):
        return self.name


class ShopingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopingcart',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='ShopingCartIngredient',
        verbose_name='Ингредиенты',
        related_name='shopingcart'
    )


class ShopingCartIngredient(models.Model):
    cart = models.ForeignKey(
        ShopingCart,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()
