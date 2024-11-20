from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from rest_framework.exceptions import ValidationError

from .base_use_case import CategoryUseCaseBase


class CreateCategoryUseCase(CategoryUseCaseBase):

    def execute(self, data):
        try:
            category = self.service.create_category(data)
            category_serialized = self.serializer(instance=category).data
            return category_serialized
        except ValidationError as e:
            raise e


class ListCategoriesUseCase(CategoryUseCaseBase):

    def execute(self, filters=None):
        categories = self.service.list_categories(filters)
        categories_serialized = self.serializer(categories, many=True).data
        return categories_serialized


class TreeCategoriesUseCase(ListCategoriesUseCase):

    def execute(self):
        categories = self.service.tree_categories()
        tree = self.build_category_tree(categories)
        self.set_tree_total_prices(tree)
        return self.serializer(instance=tree, many=True).data

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

    def set_tree_total_prices(self, queryset):
        queryset_total_price = 0
        for category in queryset:
            if not hasattr(category, "children_list"):
                queryset_total_price += category.total_price
            else:
                category_total_price = self.set_tree_total_prices(category.children_list)
                category.total_price = category_total_price
                queryset_total_price += category_total_price

        return queryset_total_price


class RetrieveByIdCategoryUseCase(CategoryUseCaseBase):

    def execute(self, target_id):
        try:
            category = self.service.get_category_by_id(target_id)
            category_serialized = self.serializer(instance=category).data
            return category_serialized
        except ObjectDoesNotExist as e:
            raise e


class UpdateByIdCategoryUseCase(CategoryUseCaseBase):

    def execute(self, target_id, data):
        try:
            category = self.service.update_category_by_id(target_id, data)
            category_serialized = self.serializer(instance=category).data
            return category_serialized
        except ObjectDoesNotExist as e:
            raise e


class DeleteCategoryUseCase(CategoryUseCaseBase):

    def execute(self, target_id):
        try:
            self.service.delete_category(target_id)
        except ObjectDoesNotExist as e:
            raise e
        except ProtectedError as e:
            raise e
