from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from common.spectacular import CombinedSchemaView
from common.urls import generate_versioned_urlpatterns
from core.settings import STATIC_ROOT

urlpatterns = [
    # -------------------------- versions --------------------------------
    *generate_versioned_urlpatterns(),

    # -------------------------- admin -----------------------------------
    path('admin/', admin.site.urls),

    # -------------------------- static / media --------------------------
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    # -------------------------- Swagger ---------------------------------
    path('swagger_yml/', CombinedSchemaView.as_view(), name='schema'),
    path('v1/swagger_yml/', SpectacularAPIView.as_view(api_version='v1'), name='schema-v1'),

    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('v1/swagger/', SpectacularSwaggerView.as_view(url_name='schema-v1'), name='swagger-v1'),

    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('v1/redoc/', SpectacularRedocView.as_view(url_name='schema-v1'), name='redoc-v1'),
]
