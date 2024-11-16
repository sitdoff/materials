from django.urls import path, reverse

from . import views

urlpatterns = [
    path("upload", views.DocumentUploadView.as_view(), name="upload-document"),
    path("status/<int:document_id>", views.DocumentCheckStatus.as_view(), name="check-status"),
]
