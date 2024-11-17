from unittest import mock

import pytest
from django.db import IntegrityError

from core.api.v1.catalog.tasks.import_materals_from_xlsx import (
    import_materials_from_xls,
)
from core.apps.catalog.models import DocumentModel


@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.openpyxl.load_workbook")
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.get_data_from_sheet")
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.get_valid_materials")
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.MaterialModel.objects.bulk_create")
@pytest.mark.django_db
def test_import_materials_from_xls_success(
    mock_bulk_create, mock_get_valid_materials, mock_get_data_from_sheet, mock_load_workbook
):
    mock_document = mock.Mock(file_path="test.xlsx")
    mock_workbook = mock.Mock()
    mock_sheet = mock.Mock()

    mock_load_workbook.return_value = mock_workbook
    mock_workbook.active = mock_sheet

    mock_get_data_from_sheet.return_value = [{"title": "Material 1", "category": 1, "code": "Code1", "price": 100}]
    mock_get_valid_materials.return_value = [mock.Mock()]

    with mock.patch(
        "core.api.v1.catalog.tasks.import_materals_from_xlsx.DocumentModel.objects.get", return_value=mock_document
    ):
        import_materials_from_xls(document_id=1)

    mock_load_workbook.assert_called_once_with("test.xlsx")
    mock_get_data_from_sheet.assert_called_once_with(mock_sheet)
    mock_get_valid_materials.assert_called_once_with(
        [{"title": "Material 1", "category": 1, "code": "Code1", "price": 100}]
    )
    mock_bulk_create.assert_called_once()
    assert mock_document.status == DocumentModel.Status.SUCCESS
    mock_document.save.assert_called()


@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.openpyxl.load_workbook", side_effect=FileNotFoundError)
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.DocumentModel.objects.get")
@pytest.mark.django_db
def test_import_materials_from_xls_file_not_found(mock_get, mock_load_workbook):
    mock_document = mock.Mock()
    mock_get.return_value = mock_document

    with pytest.raises(FileNotFoundError):
        import_materials_from_xls(document_id=1)

    assert mock_document.status == DocumentModel.Status.ERROR
    mock_document.save.assert_called()


@mock.patch(
    "core.api.v1.catalog.tasks.import_materals_from_xlsx.get_data_from_sheet", side_effect=Exception("Parsing error")
)
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.openpyxl.load_workbook")
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.DocumentModel.objects.get")
@pytest.mark.django_db
def test_import_materials_from_xls_parsing_error(mock_get, mock_load_workbook, mock_get_data_from_sheet):
    mock_document = mock.Mock()
    mock_get.return_value = mock_document
    mock_workbook = mock.Mock()
    mock_load_workbook.return_value = mock_workbook

    with pytest.raises(Exception, match="Parsing error"):
        import_materials_from_xls(document_id=1)

    assert mock_document.status == DocumentModel.Status.ERROR
    mock_document.save.assert_called()


@mock.patch(
    "core.api.v1.catalog.tasks.import_materals_from_xlsx.MaterialModel.objects.bulk_create",
    side_effect=IntegrityError,
)
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.get_valid_materials")
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.get_data_from_sheet")
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.openpyxl.load_workbook")
@mock.patch("core.api.v1.catalog.tasks.import_materals_from_xlsx.DocumentModel.objects.get")
@pytest.mark.django_db
def test_import_materials_from_xls_bulk_create_error(
    mock_get, mock_load_workbook, mock_get_data_from_sheet, mock_get_valid_materials, mock_bulk_create
):
    mock_document = mock.Mock()
    mock_get.return_value = mock_document
    mock_workbook = mock.Mock()
    mock_load_workbook.return_value = mock_workbook

    mock_get_data_from_sheet.return_value = [{"title": "Material 1", "category": 1, "code": "Code1", "price": 100}]
    mock_get_valid_materials.return_value = [mock.Mock()]

    with pytest.raises(IntegrityError):
        import_materials_from_xls(document_id=1)

    assert mock_document.status == DocumentModel.Status.ERROR
    mock_document.save.assert_called()
