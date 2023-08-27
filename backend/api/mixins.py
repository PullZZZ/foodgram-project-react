from rest_framework import mixins, viewsets


class ListDetailViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    lookup_field = 'id'
