from rest_framework import serializers

from core.apps.catalog.models import CategoryModel, MaterialModel


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialModel
        fields = ["id", "title", "code", "price", "category"]
