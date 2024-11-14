from rest_framework import serializers

from core.apps.catalog.models import DocumentModel


class DocumentSerializer(serializers.ModelSerializer):
    class Model:
        model = DocumentModel
        fields = ["id", "title", "file", "status", "created_at", "updated_at"]
