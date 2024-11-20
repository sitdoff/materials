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


def test_upload_document(document_service, document_repository):
    data = {"title": "test_file.txt", "file": mock.Mock(name="file")}

    document_repository.save_file.return_value = {"title": data["title"], "file_path": "/path/to/file"}

    document_data = document_service.upload_document(data)

    document_repository.save_file.assert_called_once_with(data)

    assert document_data["title"] == "test_file.txt"
    assert document_data["file_path"] == "/path/to/file"


@pytest.mark.django_db
def test_save(document_service, document_repository):
    document_data = {"title": "test_file.txt", "file_path": "/path/to/file"}

    document_repository.save_file_in_db = mock.Mock(
        return_value=DocumentModel(title=document_data["title"], file_path=document_data["file_path"])
    )

    document = document_service.save(document_data)

    document_repository.save_file_in_db.assert_called_once_with(title="test_file.txt", file_path="/path/to/file")

    document.title == document_data["title"]
    document.file_path == document_data["file_path"]


def test_run_task(document_service):
    with mock.patch("core.api.v1.catalog.services.import_materials_from_xls.delay_on_commit") as mock_task:
        document_service.run_task(document_id=1)
        mock_task.return_value = None
        mock_task.assert_called_once_with(1)


@pytest.mark.django_db
def test_get_document(document_service, document_repository):
    document_repository.get_document = mock.Mock(
        return_value=DocumentModel(title="test_file.txt", file_path="/path/to/file")
    )
    document = document_service.get_document(1)
    document_repository.get_document.assert_called_once_with(1)
    assert document.title == "test_file.txt"
    assert document.file_path == "/path/to/file"
