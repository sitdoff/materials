from django.db.models import DecimalField, Sum
from django.db.models.functions import Coalesce

from .base_storage import CategoryRepositoryBase


class CategoryRepository(CategoryRepositoryBase):

    def create(self, data):
        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return category

    def list(self, filters=None):
        queryset = self.model.objects.prefetch_related("materials", "children").all()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

    def tree(self):
        categories = (
            self.model.objects.annotate(
                total_price=Coalesce(
                    Sum("materials__price", output_field=DecimalField()), 0, output_field=DecimalField()
                )
            )
            .prefetch_related("materials", "children__materials")
            .order_by("tree_id", "level", "title")
        )
        return categories

    def get_by_id(self, target_id):
        return self.model.objects.get(id=target_id)

    def update_by_id(self, target_id, data):
        target = self.model.objects.filter(id=target_id)
        target.update(**data)
        return target.first()

    def delete(self, target_id):
        target = self.model.objects.get(id=target_id)
        target.delete()
