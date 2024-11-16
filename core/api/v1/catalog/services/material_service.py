from .base_service import MaterialServiceBase


class MaterialService(MaterialServiceBase):

    def create_material(self, data: dict):
        material = self.repository.create(data=data)
        return material

    def list_materials(self, filters: dict | None = None):
        return self.repository.list(filters=filters)

    def get_material_by_id(self, target_id: int):
        material = self.repository.get_by_id(target_id=target_id)
        return material

    def get_material_by_code(self, target_code: str):
        material = self.repository.get_by_code(target_code=target_code)
        return material

    def update_material_by_id(self, target_id: int, data: dict):
        return self.repository.update_by_id(target_id, data)

    def update_material_by_code(self, target_code: str, data: dict):
        return self.repository.update_by_code(target_code, data)

    def delete_material(self, target_id: int):
        self.repository.delete(target_id)
