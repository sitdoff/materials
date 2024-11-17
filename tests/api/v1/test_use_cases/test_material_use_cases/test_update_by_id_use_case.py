from unittest import mock

import pytest

from core.api.v1.catalog.use_cases.material_use_cases import UpdateByIdMaterialUseCase


@pytest.mark.django_db
def test_update_by_id_material_use_case():
    mock_service = mock.Mock()
    mock_serializer = mock.Mock()
    mock_material = mock.Mock()
    mock_service.update_material_by_id.return_value = mock_material
    mock_serializer.return_value.data = {"id": 1, "name": "Updated Material"}

    use_case = UpdateByIdMaterialUseCase(service=mock_service, serializer=mock_serializer)
    result = use_case.execute(target_id=1, data={"name": "Updated Material"})

    assert result == {"id": 1, "name": "Updated Material"}
    mock_service.update_material_by_id.assert_called_once_with(target_id=1, data={"name": "Updated Material"})
    mock_serializer.assert_called_once_with(instance=mock_material)
