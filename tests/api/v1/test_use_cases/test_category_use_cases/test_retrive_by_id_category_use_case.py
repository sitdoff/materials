from unittest import mock

import pytest
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.django_db
def test_retrieve_category_by_id_success(retrieve_by_id_usecase, mock_service, mock_serializer):
    category_id = 1
    mock_category = mock.Mock()
    mock_serialized_data = {"id": 1, "name": "Test Category"}

    mock_service.get_category_by_id.return_value = mock_category
    mock_serializer.return_value.data = mock_serialized_data

    result = retrieve_by_id_usecase.execute(category_id)

    mock_service.get_category_by_id.assert_called_once_with(category_id)
    mock_serializer.assert_called_once_with(instance=mock_category)
    assert result == mock_serialized_data


@pytest.mark.django_db
def test_retrieve_category_by_id_not_found(retrieve_by_id_usecase, mock_service):
    category_id = 1
    mock_service.get_category_by_id.side_effect = ObjectDoesNotExist("Category not found")

    with pytest.raises(ObjectDoesNotExist, match="Category not found"):
        retrieve_by_id_usecase.execute(category_id)
