import os
import re

from django.urls import path, include

from core.settings import BASE_DIR, SPECTACULAR_SETTINGS, CUSTOM_APPS


def generate_versioned_urlpatterns() -> list[path]:
    """
    Generate versioned urlpatterns for each app in CUSTOM_APPS.
    :return: Tuple of partials.
    """
    version_mask = SPECTACULAR_SETTINGS['SCHEMA_PATH_PREFIX']
    apps = CUSTOM_APPS
    paths: list[path] = []
    for app in apps:  # type: str
        paths.extend(
            path(f'{_dir}/{app}/', include((f'{app}.{_dir}.urls', app), namespace=_dir))
            for _dir in os.listdir(os.path.join(BASE_DIR, app))  # type: str
            if re.search(version_mask, _dir)
        )
    return paths
