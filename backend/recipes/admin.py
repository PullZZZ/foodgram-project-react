from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


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
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_filter = ('name', 'author', 'tags')
    list_display = (
        'author',
        'name',
        'text',
        'favorite_count'
    )

    def favorite_count(self, recipe):
        return recipe.favorite.count()


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('name',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
