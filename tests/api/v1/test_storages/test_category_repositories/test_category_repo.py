from decimal import Decimal

import pytest

from core.api.v1.catalog.storages import CategoryRepository
from core.apps.catalog.models import CategoryModel, MaterialModel


@pytest.fixture
def category_repository():
    return CategoryRepository()


@pytest.mark.django_db
def test_create_category(category_repository):
    data = {"title": "Test Category"}
    category = category_repository.create(data)

    assert category.title == "Test Category"
    assert CategoryModel.objects.count() == 1


@pytest.mark.django_db
def test_list_categories(category_repository):
    category1 = CategoryModel.objects.create(title="Category 1")
    category2 = CategoryModel.objects.create(title="Category 2")

    categories = category_repository.list()
    assert len(categories) == 2
    assert category1 in categories
    assert category2 in categories


@pytest.mark.django_db
def test_list_categories_with_filters(category_repository):
    CategoryModel.objects.create(title="Category 1")
    CategoryModel.objects.create(title="Category 2")

    filtered_categories = category_repository.list(filters={"title": "Category 1"})
    assert len(filtered_categories) == 1
    assert filtered_categories[0].title == "Category 1"


@pytest.mark.django_db
def test_tree_category_with_total_price(category_repository):
    category = CategoryModel.objects.create(title="Category")
    MaterialModel.objects.create(title="Material 1", price=Decimal("10.00"), code="a", category=category)
    MaterialModel.objects.create(title="Material 2", price=Decimal("20.00"), code="b", category=category)

    categories = category_repository.tree()
    assert len(categories) == 1
    assert categories[0].total_price == Decimal("30.00")


@pytest.mark.django_db
def test_get_by_id(category_repository):
    category = CategoryModel.objects.create(title="Category")
    retrieved_category = category_repository.get_by_id(category.id)

    assert retrieved_category == category


@pytest.mark.django_db
def test_update_by_id(category_repository):
    category = CategoryModel.objects.create(title="Old Title")
    updated_category = category_repository.update_by_id(category.id, {"title": "New Title"})

    assert updated_category.title == "New Title"
    category.refresh_from_db()
    assert category.title == "New Title"


@pytest.mark.django_db
def test_delete_category(category_repository):
    category = CategoryModel.objects.create(title="Category")
    assert CategoryModel.objects.count() == 1

    category_repository.delete(category.id)
    assert CategoryModel.objects.count() == 0
