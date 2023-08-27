from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from recipes.models import Tag
from .mixins import ListDetailViewSet
from .serializers import TagSerializer


class TagViewSet(ListDetailViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
