from django.db.models import Exists, OuterRef, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from recipes.models import Ingredient, Recipe, Tag
from users.models import Subscribe, User
from .filters import IngredientFilter, RecipeFilter
from .mixins import ListDetailViewSet
from .permissions import AuthorOrAdminOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipesSerialazer, RecipesWriteSerialazer,
                          ShoppingCartSerializer, SubscribeCreateSerializer,
                          SubscribeSerializer, TagSerializer)
from .utils import queryset_to_csv


class UserViewSet(DjoserUserViewSet):
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated:
            return queryset.annotate(
                is_subscribed=Exists(
                    user.subscribers.filter(subscribed=OuterRef('pk'))
                ))
        return queryset

    def get_permissions(self):
        if self.action == 'me':
            return (IsAuthenticated(), )
        return super().get_permissions()


class TagViewSet(ListDetailViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ListDetailViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipesViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AuthorOrAdminOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return (Recipe.objects.all().select_related('author')
                    .annotate(is_favorited=Exists(
                        user.favorite_set.filter(recipe=OuterRef('pk'))
                    ))
                    .annotate(is_in_shopping_cart=Exists(
                        user.shoppingcart_set.filter(recipe=OuterRef('pk'))
                    ))
                    .prefetch_related('tags', 'ingredients')
                    )
        return (Recipe.objects.all().select_related('author')
                .prefetch_related('tags', 'ingredients'))

    def get_serializer_class(self):
        if self.action == 'favorite':
            return FavoriteSerializer
        if self.action == 'shopping_cart':
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

        deleted, _ = request.user.favorite_set.filter(
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

        deleted, _ = request.user.shoppingcart_set.filter(
            recipe=recipe
        ).delete()
        if not deleted:
            raise ValidationError({'errors': 'Рецепт не в корзине'})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated, )
            )
    def download_shopping_cart(self, request):
        ingredients = (
            Recipe.ingredients.through.objects.filter(
                recipe__shoppingcart_set__user=request.user)
            .values('ingredient__name',
                    'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
            .order_by('ingredient__name')
        )
        if not ingredients.exists():
            raise ValidationError({'errors': 'Корзина пуста'})
        response = queryset_to_csv(ingredients)
        return response


class SubscribeViewSet(viewsets.GenericViewSet):

    lookup_field = 'pk'
    lookup_value_regex = '[0-9]+'
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'subscribe':
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

        deleted, _ = Subscribe.objects.filter(subscriber=request.user,
                                              subscribed=subscribed
                                              ).delete()
        if not deleted:
            raise ValidationError({'errors': 'Подписки не было'})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        queryset = User.objects.filter(subscribeds__subscriber=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
