from unittest import mock

import pytest
from django.core.exceptions import ValidationError

from core.api.v1.catalog.use_cases.material_use_cases import CreateMaterialUseCase


@pytest.mark.django_db
def test_create_material_use_case():
    mock_service = mock.Mock()
    mock_serializer = mock.Mock()
    mock_material = mock.Mock()
    mock_service.create_material.return_value = mock_material
    mock_serializer.return_value.data = {"id": 1, "name": "Test Material"}

    use_case = CreateMaterialUseCase(service=mock_service, serializer=mock_serializer)
    data = {"name": "Test Material"}
    result = use_case.execute(data)

    assert result == {"id": 1, "name": "Test Material"}
    mock_service.create_material.assert_called_once_with(data=data)
    mock_serializer.assert_called_once_with(instance=mock_material)


def test_create_material_use_case_validation_error():
    mock_service = mock.Mock()
    mock_serializer = mock.Mock()
    mock_service.create_material.side_effect = ValidationError("Invalid data")

    use_case = CreateMaterialUseCase(service=mock_service, serializer=mock_serializer)
    data = {"name": ""}

    with pytest.raises(ValidationError):
        use_case.execute(data)
