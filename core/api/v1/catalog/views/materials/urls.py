from django.urls import path

from core.api.v1.catalog.views.materials import views

urlpatterns = [
    path("list", views.MaterialListCreateView.as_view(), name="list-materias"),
    path("id/<int:material_id>", views.MaterialDetailByIdView.as_view(), name="retrieve-material"),
    path("code/<str:material_code>", views.MaterialDetailByCode.as_view(), name="retrieve-material"),
    path("delete/<int:material_id>", views.MaterialDeleteView.as_view(), name="delete-material"),
]
