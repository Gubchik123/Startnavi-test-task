from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("djoser.urls.jwt")),
    path("api/v1/", include("djoser.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/v1/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
