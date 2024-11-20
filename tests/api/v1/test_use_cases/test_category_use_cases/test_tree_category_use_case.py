from unittest import mock


def test_tree_categores_use_case_execute_success(tree_categories_usecase, mock_service, mock_serializer):
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

    mock_service.tree_categories = mock.Mock()
    mock_service.tree_categories.return_value = mock_categories
    mock_service.build_category_tree = mock.Mock()
    mock_service.set_tree_total_prices = mock.Mock()
    mock_serializer.return_value.data = mock_serialized_data

    result = tree_categories_usecase.execute()

    mock_service.tree_categories.assert_called_once()
    mock_service.build_category_tree.assert_called_once()
    mock_service.build_category_tree.assert_called_once_with(mock_categories)
    mock_service.set_tree_total_prices.assert_called_once()
    mock_serializer.assert_called_once_with(instance=mock.ANY, many=True)

    assert result == mock_serialized_data
