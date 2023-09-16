from django.urls import include, path
from rest_framework import routers
from .views import (IngredientViewSet, TagViewSet,
                    RecipesViewSet, SubscribeViewSet,
                    UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet, basename='recipes')
router.register('tags', TagViewSet)
router.register('users', SubscribeViewSet, basename='subscribe')
router.register('users', UserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
