import json
import re

from drf_spectacular.views import SpectacularAPIView
from rest_framework.request import Request
from rest_framework.response import Response


class CombinedSchemaView(SpectacularAPIView):
    def _get_schema_response(self, request: Request) -> Response:
        base_generator = self.generator_class(urlconf=self.urlconf, api_version=None, patterns=self.patterns)
        base_schema: dict = base_generator.get_schema(request=request, public=self.serve_public)

        if not hasattr(base_schema['components'], 'schemas'):
            base_schema['components']['schemas'] = {}
        if not hasattr(base_schema['components'], 'securitySchemes'):
            base_schema['components']['securitySchemes'] = {}

        for version in self._get_all_versions():
            version_generator = self.generator_class(urlconf=self.urlconf, api_version=version, patterns=self.patterns)
            version_schema = version_generator.get_schema(request=request, public=self.serve_public)

            dumped_data = json.dumps(version_schema)
            pattern = re.compile(r'"\$ref":\s"([#/\w]+)"')
            result = pattern.sub(r'"$ref": "\1 (' + version + r')"', dumped_data)
            version_schema = json.loads(result)

            base_schema['paths'].update(version_schema['paths'])
            base_schema['components']['securitySchemes'].update(version_schema['components'].get('securitySchemes', {}))

            for title, data in version_schema['components'].get('schemas', {}).items():
                base_schema['components']['schemas'][f'{title} ({version})'] = data

        return Response(
            data=base_schema,
            headers={"Content-Disposition": f'inline; filename="{self._get_filename(request, "all")}"'}
        )
