from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment

from common.helpers import datetime_now


def environment(**options) -> Environment:
    current_env = Environment(**options)  # noqa: S701
    current_env.globals.update(
        static=staticfiles_storage.url,
        media='',
        url=reverse,
        settings=settings,
        datetime_now=datetime_now
    )
    return current_env
