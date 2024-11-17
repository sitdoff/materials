from unittest import mock

import pytest

from core.api.v1.catalog.use_cases.category_use_cases import TreeCategoriesUseCase


@pytest.mark.django_db
def test_tree_categories_execute_success(tree_categories_usecase, mock_service, mock_serializer):
    mock_category_1 = mock.Mock(id=1, parent_id=None, total_price=0, children_list=[])
    mock_category_2 = mock.Mock(id=2, parent_id=1, total_price=100, children_list=[])
    mock_category_3 = mock.Mock(id=3, parent_id=1, total_price=200, children_list=[])
    mock_categories = [mock_category_1, mock_category_2, mock_category_3]

    mock_serialized_data = [
        {
            "id": 1,
            "total_price": 300,
            "children_list": [
                {"id": 2, "total_price": 100},
                {"id": 3, "total_price": 200},
            ],
        }
    ]

    mock_service.tree_categories.return_value = mock_categories
    mock_serializer.return_value.data = mock_serialized_data

    result = tree_categories_usecase.execute()

    mock_service.tree_categories.assert_called_once()
    mock_serializer.assert_called_once_with(instance=mock.ANY, many=True)
    assert result == mock_serialized_data


@pytest.mark.django_db
def test_tree_categories_build_category_tree():
    mock_category_1 = mock.Mock(id=1, parent_id=None)
    mock_category_2 = mock.Mock(id=2, parent_id=1)
    mock_category_3 = mock.Mock(id=3, parent_id=1)
    mock_category_1.children_list = [mock_category_2, mock_category_3]
    categories = [mock_category_1, mock_category_2, mock_category_3]

    tree = TreeCategoriesUseCase.build_category_tree(categories)

    assert len(tree) == 1
    assert tree[0].id == 1
    assert hasattr(tree[0], "children_list")
    assert len(tree[0].children_list) == 4
    assert tree[0].children_list[0].id == 2
    assert tree[0].children_list[1].id == 3


@pytest.mark.django_db
def test_tree_categories_set_tree_total_prices():
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

    use_case = TreeCategoriesUseCase()
    total_price = use_case.set_tree_total_prices(tree)

    assert total_price == 300
    assert category_1.total_price == 300
    assert category_2.total_price == 100
    assert category_3.total_price == 200
