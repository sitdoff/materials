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
        tree = self.service.build_category_tree(categories)
        self.service.set_tree_total_prices(tree)
        return self.serializer(instance=tree, many=True).data


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
