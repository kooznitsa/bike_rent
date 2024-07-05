from typing import Any, Type

from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status, views
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.serializers import Serializer

from rent.models import Rent
from rent.services.rent_bike import rent_bike
from rent.services.return_bike import return_bicycle
from .serializers import RentSerializer, BookRentSerializer, ReturnRentSerializer


class RentViewSet(viewsets.ModelViewSet):
    """Rent ViewSet"""
    model = Rent

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            return self.model.objects.filter(Q(user=self.request.user)).order_by('-finish_at')

    def get_object(self) -> Rent:
        return self.get_queryset().first()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'book_bike':
            return BookRentSerializer
        elif self.action == 'return_bike':
            return ReturnRentSerializer
        return RentSerializer

    @extend_schema(
        responses=RentSerializer,
        description='Book a bike',
    )
    @action(methods=('post',), detail=False, url_path='book_bike')
    def book_bike(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse | HttpResponse:
        """Book a bike"""
        rent = rent_bike(
            request.data.get('user'),
            request.data.get('bike'),
            request.data.get('start_at'),
            request.data.get('finish_at'),
        )

        if isinstance(rent, Rent):
            new_rent = RentSerializer(rent)
            super().create(new_rent)
            return JsonResponse(new_rent.data, status=201)
        else:
            return HttpResponse(rent.get('error'), status=422)

    @extend_schema(
        responses=RentSerializer,
        description='Return a bike',
    )
    @action(methods=('post',), detail=False, url_path='return_bike')
    def return_bike(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse | HttpResponse:
        """Return a bike"""
        rent = return_bicycle(
            request.data.get('uid'),
        )

        if isinstance(rent, Rent):
            return JsonResponse(RentSerializer(rent).data, status=200)
        else:
            return HttpResponse(rent.get('error'), status=422)

    @action(methods=('get',), detail=False, url_path='history')
    def history(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        return super().list(request, *args, **kwargs)
