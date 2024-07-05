from typing import Type, Optional, Iterable

from rest_framework.routers import SimpleRouter, Route
from rest_framework.viewsets import GenericViewSet, ViewSetMixin


class CustomRouter(SimpleRouter):

    def __init__(self) -> None:
        super().__init__()
        self.viewset_allowed_methods = {}

    def register(self, prefix: str, viewset: Type[ViewSetMixin], basename: Optional[str] = None,
                 allowed_methods: Optional[Iterable] = None) -> None:
        self.viewset_allowed_methods[viewset] = set(allowed_methods or ())
        super().register(prefix, viewset, basename=basename)

    def get_routes(self, viewset: Type[GenericViewSet]) -> list[Route]:
        original_routes = super().get_routes(viewset)
        allowed_methods = self.viewset_allowed_methods.get(viewset, set())

        # add extra actions methods to allowed methods
        for extra_action in viewset.get_extra_actions():
            allowed_methods.update(extra_action.mapping.values())

        # create new list of routes with only allowed methods
        filtered_routes = []

        for route in original_routes:
            route_mapping = {
                http_method: method_name for http_method, method_name in route.mapping.items()
                if method_name in allowed_methods  # here
            }

            if route_mapping:
                new_route = Route(
                    url=route.url,
                    mapping=route_mapping,
                    name=route.name,
                    detail=route.detail,
                    initkwargs=route.initkwargs
                )
                filtered_routes.append(new_route)

        return filtered_routes
