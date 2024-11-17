from rest_framework import serializers

from core.apps.catalog.models import MaterialModel


class MaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaterialModel
        fields = ["id", "title", "code", "price", "category"]

    def validate_category(self, value):
        if value.get_children().exists():
            raise serializers.ValidationError("Материал можно привязать только к нижней категории")
        return value
