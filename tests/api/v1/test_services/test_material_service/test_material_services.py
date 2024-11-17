from unittest import mock

import pytest

from core.api.v1.catalog.services import MaterialService
from core.api.v1.catalog.storages import MaterialRepository
from core.apps.catalog.models import MaterialModel


@pytest.fixture
def material_repository():
    return mock.create_autospec(MaterialRepository)


@pytest.fixture
def material_service(material_repository):
    return MaterialService(repository=material_repository)


@pytest.mark.django_db
def test_create_material(material_service, material_repository):
    data = {"title": "Test Material", "code": "MAT123"}
    mock_material = MaterialModel(**data)
    material_repository.create = mock.Mock(return_value=mock_material)
    material = material_service.create_material(data)
    material_repository.create.assert_called_once_with(data=data)
    assert material.title == "Test Material"
    assert material.code == "MAT123"


@pytest.mark.django_db
def test_list_materials(material_service, material_repository):
    filters = {"title": "Test Material"}
    mock_materials = [MaterialModel(title="Test Material", code="MAT123")]
    material_repository.list = mock.Mock(return_value=mock_materials)
    materials = material_service.list_materials(filters)
    material_repository.list.assert_called_once_with(filters=filters)
    assert len(materials) == 1
    assert materials[0].title == "Test Material"


@pytest.mark.django_db
def test_get_material_by_id(material_service, material_repository):
    material_id = 1
    mock_material = MaterialModel(id=material_id, title="Test Material", code="MAT123")
    material_repository.get_by_id = mock.Mock(return_value=mock_material)
    material = material_service.get_material_by_id(material_id)
    material_repository.get_by_id.assert_called_once_with(target_id=material_id)
    assert material.title == "Test Material"
    assert material.code == "MAT123"


@pytest.mark.django_db
def test_get_material_by_code(material_service, material_repository):
    material_code = "MAT123"
    mock_material = MaterialModel(code=material_code, title="Test Material")
    material_repository.get_by_code = mock.Mock(return_value=mock_material)
    material = material_service.get_material_by_code(material_code)
    material_repository.get_by_code.assert_called_once_with(target_code=material_code)
    assert material.title == "Test Material"
    assert material.code == "MAT123"


@pytest.mark.django_db
def test_update_material_by_id(material_service, material_repository):
    material_id = 1
    data = {"title": "Updated Material"}
    mock_material = MaterialModel(id=material_id, **data)
    material_repository.update_by_id = mock.Mock(return_value=mock_material)
    material = material_service.update_material_by_id(material_id, data)
    material_repository.update_by_id.assert_called_once_with(material_id, data)
    assert material.title == "Updated Material"


@pytest.mark.django_db
def test_update_material_by_code(material_service, material_repository):
    material_code = "MAT123"
    data = {"title": "Updated Material"}
    mock_material = MaterialModel(code=material_code, **data)
    material_repository.update_by_code = mock.Mock(return_value=mock_material)
    material = material_service.update_material_by_code(material_code, data)
    material_repository.update_by_code.assert_called_once_with(material_code, data)
    assert material.title == "Updated Material"


@pytest.mark.django_db
def test_delete_material(material_service, material_repository):
    material_id = 1
    material_repository.delete = mock.Mock()
    material_service.delete_material(material_id)
    material_repository.delete.assert_called_once_with(material_id)
