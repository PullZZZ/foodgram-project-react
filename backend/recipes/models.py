from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from colorfield.fields import ColorField

from users.models import User
from .validators import RecipeNameValidator


class Recipe (models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.CHARFIELD_MAX_LEN,
        validators=[RecipeNameValidator()]
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Фото'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (в минутах)',
        validators=[MinValueValidator(settings.MIN_VALUE),
                    MaxValueValidator(settings.MAX_VALUE)]
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

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created', )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(settings.MIN_VALUE),
                    MaxValueValidator(settings.MAX_VALUE)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe',
                violation_error_message=('Ингредиент может быть'
                                         'добавлен в рецепт только один раз')
            ),
        ]

    def __str__(self):
        return f'{self.recipe.name}: {self.ingredient.name} - {self.amount}'


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.CHARFIELD_MAX_LEN,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=settings.CHARFIELD_MAX_LEN
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_and_unit',
                violation_error_message=('У ингредиента может быть только одна'
                                         'единица измерения')
            ),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=settings.CHARFIELD_MAX_LEN,
        unique=True
    )
    color = ColorField(
        default='#FF0000',
        unique=True,
        verbose_name='Цвет тега'
    )
    slug = models.SlugField(
        verbose_name='Slug категории',
        max_length=settings.CHARFIELD_MAX_LEN,
        unique=True,
        null=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class AbstractUserRecipeModel(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='recipes_already_in_%(class)s'),
        ]
        abstract = True

    def __str__(self):
        return f'{self.user.username}: {self.recipe.name}'


class ShoppingCart(AbstractUserRecipeModel):

    class Meta(AbstractUserRecipeModel.Meta):
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'


class Favorite(AbstractUserRecipeModel):

    class Meta(AbstractUserRecipeModel.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
