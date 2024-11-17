import pytest
from django.db.models import ProtectedError


@pytest.mark.django_db
def test_delete_category_success(delete_category_usecase, mock_service):
    category_id = 1

    delete_category_usecase.execute(category_id)

    mock_service.delete_category.assert_called_once_with(category_id)


@pytest.mark.django_db
def test_delete_category_protected_error(delete_category_usecase, mock_service):
    category_id = 1
    mock_service.delete_category.side_effect = ProtectedError("Category is protected", category_id)

    with pytest.raises(ProtectedError, match="Category is protected"):
        delete_category_usecase.execute(category_id)
