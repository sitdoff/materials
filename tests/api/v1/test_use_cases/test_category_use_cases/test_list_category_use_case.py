from unittest import mock

import pytest


@pytest.mark.django_db
def test_list_categories_success(list_categories_usecase, mock_service, mock_serializer):
    filters = {"parent_id": None}
    mock_categories = [mock.Mock(), mock.Mock()]
    mock_serialized_data = [{"id": 1, "name": "Category 1"}, {"id": 2, "name": "Category 2"}]

    mock_service.list_categories.return_value = mock_categories
    mock_serializer.return_value.data = mock_serialized_data

    result = list_categories_usecase.execute(filters)

    mock_service.list_categories.assert_called_once_with(filters)
    mock_serializer.assert_called_once_with(mock_categories, many=True)

    assert result == mock_serialized_data
