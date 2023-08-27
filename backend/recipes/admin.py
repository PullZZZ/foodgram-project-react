from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Ingredient, Recipe, Tag, RecipeIngredient


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
    search_fields = ('name', )


class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


class IngredientAdmin(ImportExportModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    search_fields = ('name',)
    resource_classes = (IngredientResource, )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )
    list_display = (
        'author',
        'name',
        'text',
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipesAdmin)
