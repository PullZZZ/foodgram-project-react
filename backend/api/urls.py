from django.urls import include, path
from rest_framework import routers
from .views import (IngredientViewSet, TagViewSet,
                    RecipesViewSet, SubscribeViewSet,
                    FavoriteViewSet, ShoppingCartViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet)
router.register('recipes', FavoriteViewSet, basename='favorite')
router.register('recipes', ShoppingCartViewSet, basename='shopping_cart')
router.register('tags', TagViewSet)
router.register('users', SubscribeViewSet, basename='subscribe')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
