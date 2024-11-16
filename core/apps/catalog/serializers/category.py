from rest_framework import serializers

from core.apps.catalog.models import CategoryModel
from core.apps.common.serializers import BaseModelSerializer

from .material import MaterialSerializer


class CategorySerializer(BaseModelSerializer):

    class Meta:
        model = CategoryModel
        fields = ("id", "title", "level", "children", "materials")


class TreeCategorySerializer(BaseModelSerializer):
    children = serializers.SerializerMethodField()
    materials = MaterialSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CategoryModel
        fields = ("id", "title", "level", "parent", "children", "total_price", "materials")

    def get_children(self, obj):
        if hasattr(obj, "children_list"):
            return TreeCategorySerializer(obj.children_list, many=True).data
        return []
