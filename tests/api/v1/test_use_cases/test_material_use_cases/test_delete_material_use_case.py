from unittest import mock

import pytest
from django.core.exceptions import ObjectDoesNotExist

from core.api.v1.catalog.use_cases.material_use_cases import DeleteMaterialUseCase


@pytest.mark.django_db
def test_delete_material_use_case():
    mock_service = mock.Mock()
    use_case = DeleteMaterialUseCase(service=mock_service)

    use_case.execute(target_id=1)
    mock_service.delete_material.assert_called_once_with(target_id=1)


def test_delete_material_use_case_not_found():
    mock_service = mock.Mock()
    mock_service.delete_material.side_effect = ObjectDoesNotExist("Material not found")

    use_case = DeleteMaterialUseCase(service=mock_service)

    with pytest.raises(ObjectDoesNotExist):
        use_case.execute(target_id=999)
