from rest_framework import serializers

from core.apps.catalog.models import DocumentModel
from core.apps.common.serializers import BaseModelSerializer


class DocumentSerializer(BaseModelSerializer):
    file_path = serializers.CharField(write_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = DocumentModel
        fields = ["id", "title", "file_path", "status", "created_at"]
