from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()
MODEL_NAME_MAX_LEN = 200
User._meta.get_field('email')._unique = True


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
    ingredient = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
        verbose_name='Список ингредиентов',
        related_name='recipes'
    )
    tag = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        related_name='recipes'
    )

    class Meta:
        verbose_name = 'Рецепт'
        ordering = ('name', )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    cart = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()


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


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MODEL_NAME_MAX_LEN,
        db_index=True,
    )
    color = models.CharField(
        max_length=7,
        null=True
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=MODEL_NAME_MAX_LEN,
        unique=True,
        null=True
    )


class ShopingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopingcart',
    )
    ingredient = models.ManyToManyField(
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


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    subscribed = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['subscriber', 'subscribed'],
                                    name='unique_subscribe'),
            models.CheckConstraint(
                check=~models.Q(subscriber=models.F('subscribed')),
                name='self_subscribe'
            )
        ]
