from django.urls import include, path
from rest_framework import routers
from .views import TagViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('tags', TagViewSet)

urlpatterns = [
    # path('auth/', include('djoser.urls')),
    path('/', include(router.urls)),
    path('/', include('djoser.urls')),
    path('/auth/', include('djoser.urls.authtoken')),  # Работа с токенами
]
