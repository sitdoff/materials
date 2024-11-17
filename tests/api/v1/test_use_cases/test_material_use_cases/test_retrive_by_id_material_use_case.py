from unittest import mock

import pytest
from django.core.exceptions import ObjectDoesNotExist

from core.api.v1.catalog.use_cases.material_use_cases import RetrieveByIdMaterialUseCase


@pytest.mark.django_db
def test_retrieve_by_id_material_use_case():
    mock_service = mock.Mock()
    mock_serializer = mock.Mock()
    mock_material = mock.Mock()
    mock_service.get_material_by_id.return_value = mock_material
    mock_serializer.return_value.data = {"id": 1, "name": "Test Material"}

    use_case = RetrieveByIdMaterialUseCase(service=mock_service, serializer=mock_serializer)
    result = use_case.execute(target_id=1)

    assert result == {"id": 1, "name": "Test Material"}
    mock_service.get_material_by_id.assert_called_once_with(target_id=1)
    mock_serializer.assert_called_once_with(instance=mock_material)


def test_retrieve_by_id_material_use_case_not_found():
    mock_service = mock.Mock()
    mock_service.get_material_by_id.return_value = None

    use_case = RetrieveByIdMaterialUseCase(service=mock_service, serializer=mock.Mock())

    with pytest.raises(ObjectDoesNotExist):
        use_case.execute(target_id=1)
