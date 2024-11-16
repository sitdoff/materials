from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from .base_use_case import MaterialUseCaseBase


class CreateMaterialUseCase(MaterialUseCaseBase):

    def execute(self, data: dict):
        try:
            material = self.service.create_material(data=data)
            material_serialized = self.serializer(instance=material).data
            return material_serialized
        except ValidationError as e:
            raise e


class ListMateriasUseCase(MaterialUseCaseBase):

    def execute(self, filters: dict | None = None):
        materials = self.service.list_materials(filters=filters)
        materials_serialized = self.serializer(materials, many=True).data
        return materials_serialized


class RetrieveByIdMaterialUseCase(MaterialUseCaseBase):

    def execute(self, target_id: int):
        try:
            material = self.service.get_material_by_id(target_id=target_id)
            if material is None:
                raise ObjectDoesNotExist("Материал не найден")
            material_serialized = self.serializer(instance=material).data
            return material_serialized
        except ObjectDoesNotExist as e:
            raise e


class RetrieveByCodeMaterialUseCase(MaterialUseCaseBase):

    def execute(self, target_code: str):
        try:
            material = self.service.get_material_by_code(target_code=target_code)
            if material is None:
                raise ObjectDoesNotExist("Материал не найден")
            material_serialized = self.serializer(instance=material).data
            return material_serialized
        except ObjectDoesNotExist as e:
            raise e


class UpdateByIdMaterialUseCase(MaterialUseCaseBase):

    def execute(self, target_id: int, data: dict):
        try:
            material = self.service.update_material_by_id(target_id=target_id, data=data)
            material_serialized = self.serializer(instance=material).data
            return material_serialized
        except ObjectDoesNotExist as e:
            raise e


class UpdateByCodeMaterialUseCase(MaterialUseCaseBase):

    def execute(self, target_code: str, data: dict):
        try:
            material = self.service.update_material_by_code(target_code=target_code, data=data)
            material_serialized = self.serializer(instance=material).data
            return material_serialized
        except ObjectDoesNotExist as e:
            raise e


class DeleteMaterialUseCase(MaterialUseCaseBase):

    def execute(self, target_id: int):
        try:
            self.service.delete_material(target_id=target_id)
        except ObjectDoesNotExist as e:
            raise e
