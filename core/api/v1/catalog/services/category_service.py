from .base_service import CategoryServiceBase


class CategoryService(CategoryServiceBase):

    def create_category(self, data):
        category = self.repository.create(data)
        return category

    def list_categories(self, filters=None):
        return self.repository.list(filters)

    def tree_categories(self):
        return self.repository.tree()

    def build_category_tree(self, categories):
        category_dict = {category.id: category for category in categories}
        tree = []

        for category in categories:
            if category.parent_id:
                parent = category_dict[category.parent_id]
                if not hasattr(parent, "children_list"):
                    parent.children_list = []
                parent.children_list.append(category)
            else:
                tree.append(category)

        return tree

    def set_tree_total_prices(self, tree):
        parent_total_price = 0
        for category in tree:
            if not hasattr(category, "children_list"):
                parent_total_price += category.total_price
            else:
                category_total_price = self.set_tree_total_prices(category.children_list)
                category.total_price = category_total_price
                parent_total_price += category_total_price

        return parent_total_price

    def get_category_by_id(self, target_id):
        return self.repository.get_by_id(target_id)

    def update_category_by_id(self, target_id, data):
        return self.repository.update_by_id(target_id, data)

    def delete_category(self, target_id):
        self.repository.delete(target_id)
