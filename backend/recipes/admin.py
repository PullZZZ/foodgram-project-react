from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', )


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    search_fields = ('name', )
    list_filter = ('name', )
    resource_classes = (IngredientResource, )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    min_num = 1
    verbose_name = 'Ингредиенты'
    verbose_name_plural = 'Ингредиенты'


@admin.register(Recipe)
class RecipesAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_filter = ('name', 'author', 'tags')
    list_display = (
        'author',
        'name',
        'ingredients_list',
        'text',
        'favorite_count'
    )

    def favorite_count(self, recipe):
        return recipe.favorite_set.count()
    favorite_count.short_description = 'В избранном'

    def ingredients_list(self, recipe):
        return ', '.join(
            [ingredient.name for ingredient in recipe.ingredients.all()])
    ingredients_list.short_description = 'Ингредиенты'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('name',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('name',)
