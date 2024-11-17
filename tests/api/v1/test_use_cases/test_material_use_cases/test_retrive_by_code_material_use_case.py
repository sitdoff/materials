from unittest import mock

import pytest
from django.core.exceptions import ObjectDoesNotExist

from core.api.v1.catalog.use_cases.material_use_cases import (
    RetrieveByCodeMaterialUseCase,
)


@pytest.mark.django_db
def test_retrieve_by_code_material_use_case():
    mock_service = mock.Mock()
    mock_serializer = mock.Mock()
    mock_material = mock.Mock()
    mock_service.get_material_by_code.return_value = mock_material
    mock_serializer.return_value.data = {"code": "test_code", "name": "Test Material"}

    use_case = RetrieveByCodeMaterialUseCase(service=mock_service, serializer=mock_serializer)
    result = use_case.execute(target_code="test_code")

    assert result == {"code": "test_code", "name": "Test Material"}
    mock_service.get_material_by_code.assert_called_once_with(target_code="test_code")
    mock_serializer.assert_called_once_with(instance=mock_material)


def test_retrieve_by_code_material_use_case_not_found():
    mock_service = mock.Mock()
    mock_service.get_material_by_code.return_value = None

    use_case = RetrieveByCodeMaterialUseCase(service=mock_service, serializer=mock.Mock())

    with pytest.raises(ObjectDoesNotExist):
        use_case.execute(target_code="invalid_code")
