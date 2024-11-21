import os
from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest
from rest_framework.exceptions import ValidationError

from core.api.v1.catalog.storages import DocumentRepository
from core.apps.catalog.models import DocumentModel

DOCUMENT_ROOT = Path("/app/documents")
DOCUMENT_NAME_TIME_FORMAT = "%Y%m%d%H%M%S"


@pytest.fixture
def document_repository():
    return DocumentRepository()


@pytest.mark.django_db
def test_get_document_success(document_repository):
    document = DocumentModel.objects.create(title="Test Document", file_path="/test/path")
    retrieved_document = document_repository.get_by_id(document.id)
    assert retrieved_document == document


@pytest.mark.django_db
def test_get_document_not_found(document_repository):
    with pytest.raises(DocumentModel.DoesNotExist):
        document_repository.get_by_id(999)


@mock.patch("core.api.v1.catalog.storages.os.makedirs")
@mock.patch("builtins.open", new_callable=mock.mock_open)
@mock.patch("core.api.v1.catalog.storages.document_repository.datetime")
def test_save_file(mock_datetime, mock_open, mock_makedirs, document_repository):
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
    mock_file_object = mock.Mock()
    mock_file_object.name = "example.txt"
    mock_file_object.chunks.return_value = [b"chunk1", b"chunk2"]

    result = document_repository.save_file(mock_file_object)

    expected_file_name = "01012024_120000_example.txt"
    expected_file_path = os.path.join(DOCUMENT_ROOT, expected_file_name)

    mock_makedirs.assert_called_once_with(DOCUMENT_ROOT, exist_ok=True)
    mock_open.assert_called_once_with(expected_file_path, "wb+")
    handle = mock_open()
    handle.write.assert_any_call(b"chunk1")
    handle.write.assert_any_call(b"chunk2")

    assert result["title"] == expected_file_name
    assert result["file_path"] == expected_file_path


@pytest.mark.django_db
def test_create_success(document_repository):
    title = "Test Document"
    file_path = "/test/path"

    mock_serializer = mock.Mock()
    mock_serializer.is_valid.return_value = True
    mock_serializer.save.return_value = DocumentModel.objects.create(title=title, file_path=file_path)

    document_repository.serializer = mock.MagicMock()
    document_repository.serializer.return_value = mock_serializer

    document = document_repository.create(title, file_path)

    mock_serializer.is_valid.assert_called_once_with(raise_exception=True)
    assert document.title == title
    assert document.file_path == file_path


@pytest.mark.django_db
def test_create_invalid_data(document_repository):
    mock_serializer = mock.Mock()
    mock_serializer.is_valid.side_effect = ValidationError("Invalid data")

    document_repository.serializer = mock.MagicMock()
    document_repository.serializer.return_value = mock_serializer

    with pytest.raises(ValidationError, match="Invalid data"):
        document_repository.create("Invalid Title", "/invalid/path")
