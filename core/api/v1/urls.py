from django.urls import include, path

urlpatterns = [
    path("catalog/", include(("core.api.v1.catalog.urls", "catalog"), namespace="catalog")),
]
