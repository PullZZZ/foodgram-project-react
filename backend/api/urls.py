from django.urls import include, path
from rest_framework import routers
from .views import IngredientViewSet, TagViewSet, RecipesViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipesViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
