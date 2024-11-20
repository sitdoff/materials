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


def test_tree_categories(category_service, category_repository):
    mock_category_1 = mock.Mock(id=1, parent_id=None, total_price=0, children_list=[])
    mock_category_2 = mock.Mock(id=2, parent_id=1, total_price=100, children_list=[])
    mock_category_3 = mock.Mock(id=3, parent_id=1, total_price=200, children_list=[])
    mock_categories = [mock_category_1, mock_category_2, mock_category_3]
    category_repository.tree = mock.Mock(return_value=mock_categories)

    categories = category_service.tree_categories()

    category_repository.tree.assert_called_once()

    assert len(categories) == 3
    assert categories[0].id == 1


def test_build_category_tree(category_service):
    mock_category_1 = mock.Mock(id=1, parent_id=None)
    mock_category_2 = mock.Mock(id=2, parent_id=1)
    mock_category_3 = mock.Mock(id=3, parent_id=1)
    mock_category_1.children_list = [mock_category_2, mock_category_3]
    categories = [mock_category_1, mock_category_2, mock_category_3]

    tree = category_service.build_category_tree(categories)

    assert len(tree) == 1
    assert tree[0].id == 1
    assert hasattr(tree[0], "children_list")
    assert len(tree[0].children_list) == 4
    assert tree[0].children_list[0].id == 2
    assert tree[0].children_list[1].id == 3


def test_set_tree_total_prices(category_service):
    class Category:
        def __init__(self, id, total_price, children_list=None):
            self.id = id
            self.total_price = total_price
            if children_list:
                self.children_list = children_list

    category_2 = Category(id=2, total_price=100)
    category_3 = Category(id=3, total_price=200)
    category_1 = Category(id=1, total_price=0, children_list=[category_2, category_3])
    tree = [category_1]

    total_price = category_service.set_tree_total_prices(tree)

    assert total_price == 300
    assert category_1.total_price == 300
    assert category_2.total_price == 100
    assert category_3.total_price == 200
