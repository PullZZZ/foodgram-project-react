from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Tag, Recipe
from users.models import Subscribe, User
from .filters import IngredientFilter, RecipeFilter
from .mixins import ListDetailViewSet
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipesSerialazer, RecipesWriteSerialazer,
                          SubscribeSerializer, SubscribeCreateSerializer,
                          ShoppingCartSerializer, FavoriteSerializer)


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
    serializer_class = RecipesSerialazer
    queryset = Recipe.objects.all()
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('favorite', ):
            return FavoriteSerializer
        if self.action in ('shopping_cart', ):
            return ShoppingCartSerializer
        if self.action in ('list', 'retrieve'):
            return RecipesSerialazer
        return RecipesWriteSerialazer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            data = {'recipe': recipe.id}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        deleted, _ = request.user.favorite.filter(
            recipe=recipe
        ).delete()
        if not deleted:
            raise ValidationError({'errors': 'Рецепт не в избранном'})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            data = {'recipe': recipe.id}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        deleted, _ = request.user.shoppingcart.filter(
            recipe=recipe
        ).delete()
        if not deleted:
            raise ValidationError({'errors': 'Рецепт не в корзине'})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        pass


class SubscribeViewSet(viewsets.GenericViewSet):

    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'

    def get_serializer_class(self):
        if self.action in ('subscribe', ):
            return SubscribeCreateSerializer
        return SubscribeSerializer

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, pk):
        subscribed = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            data = {'subscribed': subscribed.id}
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(subscriber=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            deleted, _ = Subscribe.objects.filter(subscriber=request.user,
                                                  subscribed=subscribed
                                                  ).delete()
            if not deleted:
                raise ValidationError({'errors': 'Подписки не было'})
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribed__subscriber=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
