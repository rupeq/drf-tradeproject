from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import *


class UserView(viewsets.GenericViewSet,
               viewsets.mixins.CreateModelMixin,
               viewsets.mixins.ListModelMixin,
               viewsets.mixins.RetrieveModelMixin,
               viewsets.mixins.UpdateModelMixin):

    queryset = User.objects.all()

    default_serializer_class = UserSerializer

    serializer_classes_by_action = {
        "list": ListUserSerializer,
        "create": UserSerializer,
        "retrieve": UserSerializer,
        "update": UpdateUserSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, self.default_serializer_class)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
