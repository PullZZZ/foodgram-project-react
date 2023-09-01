from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Tag, Recipe, Favorite, ShoppingCart
from users.models import Subscribe, User
from .filters import IngredientFilter, RecipeFilter
from .mixins import ListDetailViewSet
from .serializers import (IngredientSerializer, TagSerializer,
                          RecipesSerialazer, RecipesShortSerialazer,
                          RecipesWriteSerialazer, SubscribeSerializer)


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
        if self.action in ('favorite','shopping_cart', ):
            return RecipesShortSerialazer
        if self.action in ('list', 'retrieve'):
            return RecipesSerialazer
        return RecipesWriteSerialazer
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def update(self, request, *args, **kwargs):
    #     print('full')
    #     response = {'message': 'Method not allowed'}
    #     return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        queryset = Favorite.objects.filter(user=request.user,
                                           recipe=recipe)
        if request.method == 'POST':
            if queryset.exists():
                raise ValidationError({'errors': 'Рецепт уже в избранном'})
            Favorite.objects.create(user=request.user,
                                    recipe=recipe)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if queryset.exists():
                queryset.delete()
            else:
                raise ValidationError({'errors': 'Рецепт не в избранном'})
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        queryset = ShoppingCart.objects.filter(user=request.user,
                                               recipe=recipe)
        if request.method == 'POST':
            if queryset.exists():
                raise ValidationError({'errors': 'Рецепт уже в корзине'})
            ShoppingCart.objects.create(user=request.user,
                                        recipe=recipe)
            serializer = self.get_serializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if queryset.exists():
                queryset.delete()
            else:
                raise ValidationError({'errors': 'Этого рецепта в нет корзине'})
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        pass


class SubscribeViewSet(viewsets.GenericViewSet):

    serializer_class = SubscribeSerializer
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, pk):
        subscribed = get_object_or_404(User, pk=pk)
        queryset = Subscribe.objects.filter(subscriber=request.user,
                                            subscribed=subscribed)
        if request.method == 'POST':
            if (request.user == subscribed):
                raise ValidationError(
                    {'errors': 'Нельзя подписаться на самого себя'})
            if queryset.exists():
                raise ValidationError({'errors': 'Подписка уже оформлена'})
            Subscribe.objects.create(subscriber=request.user,
                                     subscribed=subscribed)
            serializer = self.get_serializer(subscribed)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if queryset.exists():
                queryset.delete()
            else:
                raise ValidationError({'errors': 'Подписки не было'})
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribed__subscriber=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
