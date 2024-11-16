from django.urls import path

from core.api.v1.catalog.views.categories import views

urlpatterns = [
    path("list", views.CategoryListCreateView.as_view(), name="list-categories"),
    path("tree", views.CategoryTreeCreateView.as_view(), name="tree-categories"),
    path("id/<int:category_id>", views.CategoryDetailByIdView.as_view(), name="retrieve-category>"),
    path("delete/<int:category_id>", views.CategoryDeleteView.as_view(), name="delete-category"),
]
