from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_create_category_success(create_category_usecase, mock_service, mock_serializer):
    data = {"name": "Test Category"}
    mock_category = mock.Mock()
    mock_serialized_data = {"id": 1, "name": "Test Category"}

    mock_service.create_category.return_value = mock_category
    mock_serializer.return_value.data = mock_serialized_data

    result = create_category_usecase.execute(data)

    mock_service.create_category.assert_called_once_with(data)
    mock_serializer.assert_called_once_with(instance=mock_category)
    assert result == mock_serialized_data


@pytest.mark.django_db
def test_create_category_validation_error(create_category_usecase, mock_service):
    data = {"name": ""}
    mock_service.create_category.side_effect = ValidationError("Invalid data")

    with pytest.raises(ValidationError, match="Invalid data"):
        create_category_usecase.execute(data)
