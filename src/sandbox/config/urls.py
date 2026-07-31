from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from core import views as core_views

urlpatterns = [
    path("", include("core.urls", namespace="core")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("forms/", include("public_forms.urls", namespace="public_forms")),
    path("showcase/", include("ui_showcase.urls", namespace="ui_showcase")),
    path("qa/", include("qa_orchestrator.urls", namespace="qa_orchestrator")),
    path("search/", core_views.SiteSearchView.as_view(), name="site_search"),
    path(
        "search/autocomplete/",
        core_views.site_index_autocomplete,
        name="site_index_autocomplete",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
