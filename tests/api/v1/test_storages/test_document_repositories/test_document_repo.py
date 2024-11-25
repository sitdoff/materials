from datetime import datetime
from pathlib import Path
from unittest import mock

import pytest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from core.api.v1.catalog.storages import DocumentRepository

DOCUMENT_ROOT = Path("/app/documents")
DOCUMENT_NAME_TIME_FORMAT = "%Y%m%d%H%M%S"


@pytest.fixture
def mock_model():
    return mock.MagicMock()


@pytest.fixture
def document_repository():
    return DocumentRepository()


@pytest.mark.django_db
def test_get_by_id_success(document_repository: DocumentRepository, mock_model):
    document_repository.model = mock_model
    mock_document = mock.MagicMock()
    mock_model.objects.get.return_value = mock_document

    result = document_repository.get_by_id(1)

    assert result == mock_document
    mock_model.objects.get.assert_called_once_with(pk=1)


@pytest.mark.django_db
def test_get_by_id_not_found(document_repository: DocumentRepository, mock_model):
    mock_model.objects.get.side_effect = ObjectDoesNotExist()
    document_repository.model = mock_model

    with pytest.raises(ObjectDoesNotExist):
        document_repository.get_by_id(1)

    mock_model.objects.get.assert_called_once_with(pk=1)


@mock.patch("core.api.v1.catalog.storages.document_repository.DocumentSerializer")
@pytest.mark.django_db
def test_create_success(mock_serializer_class, document_repository: DocumentRepository):
    mock_serializer = mock.MagicMock()
    mock_serializer.is_valid.return_value = True
    mock_document = mock.MagicMock()
    mock_serializer.save.return_value = mock_document
    mock_serializer_class.return_value = mock_serializer

    mock_file = mock.MagicMock()
    mock_file.name = "test.xlsx"
    data = {"file": mock_file}

    with mock.patch("core.api.v1.catalog.storages.document_repository.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

        result = document_repository.create(data)

    assert result == mock_document
    assert data["file"].name == "01012024_120000_test.xlsx"
    mock_serializer_class.assert_called_once_with(data=data)
    mock_serializer.is_valid.assert_called_once()
    mock_serializer.save.assert_called_once()


@mock.patch("core.api.v1.catalog.storages.document_repository.DocumentSerializer")
@pytest.mark.django_db
def test_create_invalid_data(mock_serializer_class, document_repository: DocumentRepository):
    mock_serializer = mock.MagicMock()
    mock_serializer.is_valid.side_effect = ValidationError
    mock_serializer_class.return_value = mock_serializer

    mock_file = mock.MagicMock()
    mock_file.name = "test.xlsx"
    data = {"file": mock_file}

    with pytest.raises(ValidationError):
        document_repository.create(data)

    mock_serializer_class.assert_called_once_with(data=data)
    mock_serializer.is_valid.assert_called_once()
    mock_serializer.save.assert_not_called()


@pytest.mark.django_db
def test_list(document_repository: DocumentRepository, mock_model):
    document_repository.model = mock_model
    mock_queryset = [mock.MagicMock(), mock.MagicMock()]
    mock_model.objects.all.return_value = mock_queryset

    result = document_repository.list()

    assert result == mock_queryset
    mock_model.objects.all.assert_called_once()
