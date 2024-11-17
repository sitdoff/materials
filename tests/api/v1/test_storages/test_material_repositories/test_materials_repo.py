import pytest
from rest_framework.exceptions import ValidationError

from core.api.v1.catalog.storages import MaterialRepository
from core.apps.catalog.models import CategoryModel


@pytest.fixture
def category():
    return CategoryModel.objects.create(title="Category 1")


@pytest.fixture
def material_data(category):
    return {
        "title": "Material 1",
        "category": category.id,
        "code": "123ABC",
        "price": 100.0,
    }


@pytest.fixture
def material_repository():
    return MaterialRepository()


@pytest.mark.django_db
def test_create(material_repository, material_data):
    result = material_repository.create(material_data)

    assert result.title == material_data["title"]
    assert result.code == material_data["code"]
    assert result.price == material_data["price"]


@pytest.mark.django_db
def test_create_invalid(material_repository):
    invalid_data = {
        "title": "Invalid Material",
        "category": 1,
        "price": 100.0,
    }

    with pytest.raises(ValidationError):
        material_repository.create(invalid_data)


@pytest.mark.django_db
def test_list(material_repository, material_data):
    material_repository.create(material_data)
    result = material_repository.list()

    assert len(result) > 0
    assert result[0].title == material_data["title"]


@pytest.mark.django_db
def test_list_with_filters(material_repository, material_data):
    material_repository.create(material_data)
    filters = {"code": material_data["code"]}
    result = material_repository.list(filters=filters)

    assert len(result) == 1
    assert result[0].code == material_data["code"]


@pytest.mark.django_db
def test_get_by_id(material_repository, material_data):
    material = material_repository.create(material_data)
    result = material_repository.get_by_id(material.id)

    assert result is not None
    assert result.id == material.id


@pytest.mark.django_db
def test_get_by_id_not_found(material_repository):
    result = material_repository.get_by_id(99999)

    assert result is None


@pytest.mark.django_db
def test_get_by_code(material_repository, material_data):
    material = material_repository.create(material_data)
    result = material_repository.get_by_code(material.code)

    assert result is not None
    assert result.code == material.code


@pytest.mark.django_db
def test_get_by_code_not_found(material_repository):
    result = material_repository.get_by_code("nonexistent_code")

    assert result is None


@pytest.mark.django_db
def test_update_by_id(material_repository, material_data):
    material = material_repository.create(material_data)
    updated_data = {"price": 150.0}
    result = material_repository.update_by_id(material.id, updated_data)

    assert result.price == 150.0


@pytest.mark.django_db
def test_update_by_code(material_repository, material_data):
    material = material_repository.create(material_data)
    updated_data = {"price": 200.0}
    result = material_repository.update_by_code(material.code, updated_data)

    assert result.price == 200.0


@pytest.mark.django_db
def test_delete(material_repository, material_data):
    material = material_repository.create(material_data)
    material_repository.delete(material.id)

    result = material_repository.get_by_id(material.id)
    assert result is None
