from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Third-party apps
    path("api/v1/", include("djoser.urls.jwt")),
    path("api/v1/", include("djoser.urls")),
    # Local apps
    path("api/v1/", include("post.router")),
    path("api/v1/", include("comment.router")),
    # Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG and settings.DEVELOPMENT and not settings.TESTING:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
