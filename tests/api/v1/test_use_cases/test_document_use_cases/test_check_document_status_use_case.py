from unittest import mock

import pytest
from django.core.exceptions import ObjectDoesNotExist


@pytest.mark.django_db
def test_check_document_status_success(check_document_status_usecase, mock_service, mock_serializer):
    document_id = 1
    mock_document = mock.Mock(id=document_id, title="Test Document")
    mock_serialized_data = {"id": 1, "title": "Test Document"}

    mock_service.repository.get_by_id.return_value = mock_document
    mock_serializer.return_value.data = mock_serialized_data

    result = check_document_status_usecase.execute(document_id)

    mock_service.repository.get_by_id.assert_called_once_with(document_id)

    mock_serializer.assert_called_once_with(instance=mock_document)

    assert result == mock_serialized_data


@pytest.mark.django_db
def test_check_document_status_not_found(check_document_status_usecase, mock_service):
    document_id = 1
    mock_service.repository.get_by_id.side_effect = ObjectDoesNotExist("Document not found")

    with pytest.raises(ObjectDoesNotExist, match="Document not found"):
        check_document_status_usecase.execute(document_id)
