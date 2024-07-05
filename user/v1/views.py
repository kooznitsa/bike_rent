from typing import Any, Type

from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action
from rest_framework.request import Request

from user.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User ViewSet"""
    model = User
    serializer_class = UserSerializer
    queryset = model.objects.active()

    def get_object(self) -> User:
        return self.request.user

    @action(methods=('get',), detail=False, url_path='info')
    def info(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('patch',), detail=False, url_path='edit')
    def edit(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        return super().partial_update(request, *args, **kwargs)

    @action(methods=('delete',), detail=False, url_path='delete')
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=('is_active',))

        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
