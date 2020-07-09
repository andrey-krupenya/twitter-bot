from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from app_for_trafic.utils.auth import CustomSessionAuthentication

api_info = openapi.Info(
       title="TWITTER BOT SERVICE API",
       default_version='v1',
       description="Builded with pleasure",
       terms_of_service="https://ak.rv.ua",
       contact=openapi.Contact(email="krupenya.public@gmail.com"),
       license=openapi.License(name="BSD License"),
    )

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(CustomSessionAuthentication,),
)

urlpatterns_swagger = [
   url(r'^apidocs/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^apidocs/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^apidocs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
