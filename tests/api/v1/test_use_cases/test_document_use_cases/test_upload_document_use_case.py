from unittest import mock

import pytest
from django.urls import reverse
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_upload_document_success(upload_document_usecase, mock_service, mock_serializer):
    file = mock.Mock()
    mock_document = mock.Mock(id=1, pk=1, title="Test Document")
    document_data = {"title": "Test Document", "file_path": "/path/to/file"}
    mock_serialized_data = {"id": 1, "title": "Test Document"}

    mock_service.upload_document.return_value = document_data
    mock_service.save.return_value = mock_document
    mock_service.run_task.return_value = None

    mock_serializer.return_value.data = mock_serialized_data

    result = upload_document_usecase.execute(file)

    mock_service.upload_document.assert_called_once_with(file)
    mock_service.save.assert_called_once_with(document_data)
    mock_service.run_task.assert_called_once_with(mock_document.pk)

    mock_serializer.assert_called_once_with(instance=mock_document)

    expected_result = mock_serialized_data.copy()
    expected_result["check_status"] = reverse(
        "api:v1:catalog:documents:check-status", kwargs={"document_id": mock_serialized_data["id"]}
    )
    assert result == expected_result


@pytest.mark.django_db
def test_upload_document_validation_error(upload_document_usecase, mock_service):
    file = mock.Mock()
    mock_service.upload_document.side_effect = ValidationError("Invalid file")

    with pytest.raises(ValidationError, match="Invalid file"):
        upload_document_usecase.execute(file)

    upload_document_usecase.serializer.assert_not_called()
