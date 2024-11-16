from .base_storage import MaterialRepositoryBase


class MaterialRepository(MaterialRepositoryBase):
    def create(self, data: dict):
        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)
        material = serializer.save()
        return material

    def list(self, filters: dict | None = None):
        queryset = self.model.objects.all()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

    def get_by_id(self, target_id: int):
        return self.model.objects.filter(id=target_id).first()

    def get_by_code(self, target_code: str):
        return self.model.objects.filter(code=target_code).first()

    def update_by_id(self, target_id: int, data: dict):
        target = self.model.objects.filter(id=target_id)
        target.update(**data)
        return target.first()

    def update_by_code(self, target_code: str, data: dict):
        target = self.model.objects.filter(code=target_code)
        target.update(**data)
        return target.first()

    def delete(self, target_id: int):
        target = self.model.objects.get(id=target_id)
        target.delete()
