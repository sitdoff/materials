from django.urls import include, path

urlpatterns = [
    path("materials/", include(("core.api.v1.catalog.views.materials.urls", "materials"), namespace="materials")),
    path("categories/", include(("core.api.v1.catalog.views.categories.urls", "categories"), namespace="categories")),
    path("documents/", include(("core.api.v1.catalog.views.document.urls", "documents"), namespace="documents")),
]
