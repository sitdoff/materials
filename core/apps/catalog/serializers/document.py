from rest_framework import serializers

from core.apps.catalog.models import DocumentModel


class DocumentSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = DocumentModel
        fields = ["id", "title", "file_path", "status", "created_at"]
