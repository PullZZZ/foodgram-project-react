from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Tag, Recipe
from .filters import IngredientFilter
from .mixins import ListDetailViewSet
from .serializers import IngredientSerializer, TagSerializer, RecipesSerialazer


class TagViewSet(ListDetailViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListDetailViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerialazer
