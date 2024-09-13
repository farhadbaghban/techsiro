from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="TECH SIRO",
        default_version="v1",
        description="TECHSIRO API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="baghbanfarhad@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path(f"{settings.PROJECT_URL_PREFIX}admin/", admin.site.urls),
    path(
        f"{settings.PROJECT_URL_PREFIX}auth/",
        include("projectApps.accounts.api.urls", namespace="AccountUserApi"),
    ),
]


urlpatterns += [
    path(
        f"{settings.PROJECT_URL_PREFIX}swagger.json/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        f"{settings.PROJECT_URL_PREFIX}swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        f"{settings.PROJECT_URL_PREFIX}redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
