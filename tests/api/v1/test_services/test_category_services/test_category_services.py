from unittest import mock

import pytest

from core.api.v1.catalog.services import CategoryService
from core.api.v1.catalog.storages import CategoryRepository
from core.apps.catalog.models import CategoryModel


@pytest.fixture
def category_repository():
    return mock.create_autospec(CategoryRepository)


@pytest.fixture
def category_service(category_repository):
    return CategoryService(repository=category_repository)


@pytest.mark.django_db
def test_create_category(category_service, category_repository):
    data = {"title": "Test Category"}
    mock_category = CategoryModel(**data)
    category_repository.create = mock.Mock(return_value=mock_category)
    category = category_service.create_category(data)
    category_repository.create.assert_called_once_with(data)
    assert category.title == "Test Category"


@pytest.mark.django_db
def test_list_categories(category_service, category_repository):
    filters = {"title": "Test Category"}
    mock_categories = [CategoryModel(title="Test Category")]
    category_repository.list = mock.Mock(return_value=mock_categories)
    categories = category_service.list_categories(filters)
    category_repository.list.assert_called_once_with(filters)
    assert len(categories) == 1
    assert categories[0].title == "Test Category"


@pytest.mark.django_db
def test_tree_categories(category_service, category_repository):
    mock_categories = [CategoryModel(title="Test Category")]
    category_repository.tree = mock.Mock(return_value=mock_categories)
    categories = category_service.tree_categories()
    category_repository.tree.assert_called_once()
    assert len(categories) == 1
    assert categories[0].title == "Test Category"


@pytest.mark.django_db
def test_get_category_by_id(category_service, category_repository):
    category_id = 1
    mock_category = CategoryModel(id=category_id, title="Test Category")
    category_repository.get_by_id = mock.Mock(return_value=mock_category)
    category = category_service.get_category_by_id(category_id)
    category_repository.get_by_id.assert_called_once_with(category_id)
    assert category.title == "Test Category"


@pytest.mark.django_db
def test_update_category_by_id(category_service, category_repository):
    category_id = 1
    data = {"title": "Updated Category"}
    mock_category = CategoryModel(id=category_id, **data)
    category_repository.update_by_id = mock.Mock(return_value=mock_category)
    category = category_service.update_category_by_id(category_id, data)
    category_repository.update_by_id.assert_called_once_with(category_id, data)
    assert category.title == "Updated Category"


@pytest.mark.django_db
def test_delete_category(category_service, category_repository):
    category_id = 1
    category_repository.delete = mock.Mock()
    category_service.delete_category(category_id)
    category_repository.delete.assert_called_once_with(category_id)
