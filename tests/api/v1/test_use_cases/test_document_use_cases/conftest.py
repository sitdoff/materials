from unittest import mock

import pytest

from core.api.v1.catalog.use_cases import (
    CheckDocumentStatusUseCase,
    UploadDocumentUseCase,
)


@pytest.fixture
def mock_service():
    return mock.Mock()


@pytest.fixture
def mock_serializer():
    return mock.Mock()


@pytest.fixture
def upload_document_usecase(mock_service, mock_serializer):
    return UploadDocumentUseCase(service=mock_service, serializer=mock_serializer)


@pytest.fixture
def check_document_status_usecase(mock_service, mock_serializer):
    return CheckDocumentStatusUseCase(service=mock_service, serializer=mock_serializer)
