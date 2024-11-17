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
def test_save_document(document_service, document_repository):
    document_repository.save_file = mock.Mock(return_value={"title": "test_file.txt", "file_path": "/path/to/file"})
    document_repository.save_file_in_db = mock.Mock(
        return_value=DocumentModel(title="test_file.txt", file_path="/path/to/file")
    )

    with mock.patch("core.api.v1.catalog.services.import_materials_from_xls.delay_on_commit") as mock_task:
        mock_task.return_value = None

        data = {"title": "test_file.txt", "file": mock.Mock(name="file")}

        document = document_service.save_document(data)

        document_repository.save_file.assert_called_once_with(data)
        document_repository.save_file_in_db.assert_called_once_with(title="test_file.txt", file_path="/path/to/file")
        mock_task.assert_called_once_with(document.pk)

        assert document.title == "test_file.txt"
        assert document.file_path == "/path/to/file"


@pytest.mark.django_db
def test_get_document(document_service, document_repository):
    document_repository.get_document = mock.Mock(
        return_value=DocumentModel(title="test_file.txt", file_path="/path/to/file")
    )
    document = document_service.get_document(1)
    document_repository.get_document.assert_called_once_with(1)
    assert document.title == "test_file.txt"
    assert document.file_path == "/path/to/file"
