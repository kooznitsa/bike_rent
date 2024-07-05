from datetime import datetime, timedelta
from typing import Any

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
import pytz
from rest_framework import filters, permissions, viewsets
from rest_framework.request import Request

from bike.models import Bike
from bike.v1.filters import BikeFilter
from bike.v1.serializers import BikeSerializer
from rent.models import Rent


class BikeViewSet(viewsets.ReadOnlyModelViewSet):
    """Bike ViewSet"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = BikeSerializer
    model = serializer_class.Meta.model
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = BikeFilter

    def get_queryset(self):
        now = datetime.now(tz=pytz.timezone('Europe/Moscow'))

        booked_rents = Rent.objects.filter(
            status__in=('created', 'confirmed', 'current'),
            start_at__lte=self.request.GET.get(
                'start_at__gte',
                now.strftime('%Y-%m-%dT%H:%M:%S')
            ),
            finish_at__gte=self.request.GET.get(
                'finish_at__lte',
                (now + timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%S')
            ),
        )
        booked_bikes_uids = [i.bike.uid for i in booked_rents]

        return Bike.objects.exclude(uid__in=booked_bikes_uids)

    @extend_schema(
        responses=serializer_class,
        parameters=[
            OpenApiParameter(
                name='start_at__gte',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
            OpenApiParameter(
                name='finish_at__lte',
                type=OpenApiTypes.DATETIME,
                location=OpenApiParameter.QUERY,
                required=False,
            ),
        ],
    )
    def list(self, request: Request, *args: Any, **kwargs: Any) -> JsonResponse:
        return super().list(request, *args, **kwargs)
