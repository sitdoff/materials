from unittest import mock

import pytest

from core.api.v1.catalog.services import DocumentService
from core.api.v1.catalog.storages import DocumentRepository
from core.apps.catalog.models import DocumentModel


@pytest.fixture
def document_repository():
    return mock.create_autospec(DocumentRepository)


@pytest.fixture
def document_service(document_repository):
    return DocumentService(repository=document_repository)


@pytest.mark.django_db
def test_save(document_service, document_repository):
    mock_file = mock.MagicMock()
    mock_file.name = "test_file.xlxs"
    document_data = {"title": mock_file}

    document_repository.create = mock.Mock(return_value=DocumentModel(file=mock_file))

    document = document_service.save(document_data)

    assert isinstance(document, DocumentModel)
    document_repository.create.assert_called_once_with(document_data)


def test_run_task(document_service):
    pass


@pytest.mark.django_db
def test_get_document(document_service, document_repository):
    mock_file = mock.MagicMock()
    mock_file.name = "test_file.xlxs"

    document_repository.get_by_id = mock.Mock(return_value=DocumentModel(file=mock_file))

    document_service.get_document(1)

    document_repository.get_by_id.assert_called_once_with(1)
