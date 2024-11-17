from unittest import mock

import pytest

from core.api.v1.catalog.use_cases.material_use_cases import ListMateriasUseCase


@pytest.mark.django_db
def test_list_materials_use_case():
    mock_service = mock.Mock()
    mock_serializer = mock.Mock()
    mock_materials = [mock.Mock(), mock.Mock()]
    mock_service.list_materials.return_value = mock_materials
    mock_serializer.return_value.data = [{"id": 1}, {"id": 2}]

    use_case = ListMateriasUseCase(service=mock_service, serializer=mock_serializer)
    result = use_case.execute(filters={"category": "test"})

    assert result == [{"id": 1}, {"id": 2}]
    mock_service.list_materials.assert_called_once_with(filters={"category": "test"})
    mock_serializer.assert_called_once_with(mock_materials, many=True)
