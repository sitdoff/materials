from .base_service import CategoryServiceBase


class CategoryService(CategoryServiceBase):

    def create_category(self, data):
        category = self.repository.create(data)
        return category

    def list_categories(self, filters=None):
        return self.repository.list(filters)

    def tree_categories(self):
        return self.repository.tree()

    def get_category_by_id(self, target_id):
        return self.repository.get_by_id(target_id)

    def update_category_by_id(self, target_id, data):
        return self.repository.update_by_id(target_id, data)

    def delete_category(self, target_id):
        self.repository.delete(target_id)
