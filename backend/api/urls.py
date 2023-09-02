from django.urls import include, path
from rest_framework import routers
from .views import (IngredientViewSet, TagViewSet,
                    RecipesViewSet, SubscribeViewSet,
                    UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet)
router.register('tags', TagViewSet)
router.register('users', UserViewSet)
router.register('users', SubscribeViewSet, basename='subscribe')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
