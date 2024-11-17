from unittest import mock

import pytest

from core.api.v1.catalog.use_cases.category_use_cases import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    ListCategoriesUseCase,
    RetrieveByIdCategoryUseCase,
    TreeCategoriesUseCase,
    UpdateByIdCategoryUseCase,
)


@pytest.fixture
def mock_service():
    return mock.Mock()


@pytest.fixture
def mock_serializer():
    return mock.Mock()


@pytest.fixture
def create_category_usecase(mock_service, mock_serializer):
    return CreateCategoryUseCase(service=mock_service, serializer=mock_serializer)


@pytest.fixture
def list_categories_usecase(mock_service, mock_serializer):
    return ListCategoriesUseCase(service=mock_service, serializer=mock_serializer)


@pytest.fixture
def tree_categories_usecase(mock_service, mock_serializer):
    return TreeCategoriesUseCase(service=mock_service, serializer=mock_serializer)


@pytest.fixture
def retrieve_by_id_usecase(mock_service, mock_serializer):
    return RetrieveByIdCategoryUseCase(service=mock_service, serializer=mock_serializer)


@pytest.fixture
def update_by_id_usecase(mock_service, mock_serializer):
    return UpdateByIdCategoryUseCase(service=mock_service, serializer=mock_serializer)


@pytest.fixture
def delete_category_usecase(mock_service):
    return DeleteCategoryUseCase(service=mock_service)
