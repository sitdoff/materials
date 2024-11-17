from unittest import mock

import pytest


@pytest.mark.django_db
def test_update_category_by_id_success(update_by_id_usecase, mock_service, mock_serializer):
    category_id = 1
    data = {"name": "Updated Category"}
    mock_category = mock.Mock()
    mock_serialized_data = {"id": 1, "name": "Updated Category"}

    mock_service.update_category_by_id.return_value = mock_category
    mock_serializer.return_value.data = mock_serialized_data

    result = update_by_id_usecase.execute(category_id, data)

    mock_service.update_category_by_id.assert_called_once_with(category_id, data)
    mock_serializer.assert_called_once_with(instance=mock_category)
    assert result == mock_serialized_data
