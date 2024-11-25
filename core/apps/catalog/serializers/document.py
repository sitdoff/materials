from rest_framework import serializers

from core.apps.catalog.models import DocumentModel
from core.apps.common.serializers import BaseModelSerializer


class DocumentSerializer(BaseModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = DocumentModel
        fields = ["id", "file", "status", "created_at"]
