from unittest.mock import MagicMock, patch

import pytest

from core.api.v1.catalog.tasks.import_materials_from_xlsx import (
    import_materials_from_xls,
)
from core.apps.catalog.models import DocumentModel, MaterialModel


@pytest.fixture
def mock_tempfile():
    # Мок временного файла
    tmp_file = MagicMock()
    tmp_file.__enter__.return_value = tmp_file
    tmp_file.__exit__ = MagicMock()
    tmp_file.name = "/tmp/mockfile.xlsx"
    with patch(
        "core.api.v1.catalog.tasks.import_materials_from_xlsx.tempfile.NamedTemporaryFile", return_value=tmp_file
    ):
        yield tmp_file


@pytest.fixture
def mock_openpyxl():
    # Мок для openpyxl
    mock_workbook = MagicMock()
    mock_sheet = MagicMock()
    mock_workbook.active = mock_sheet
    with patch(
        "core.api.v1.catalog.tasks.import_materials_from_xlsx.openpyxl.load_workbook", return_value=mock_workbook
    ):
        yield mock_sheet


@pytest.fixture
def mock_get_s3_data_from_env():
    with patch("core.api.v1.catalog.tasks.import_materials_from_xlsx.get_s3_data_from_env") as mock:
        s3_client = MagicMock()
        s3_client.get_object.return_value = {"Body": MagicMock(read=lambda: b"Mocked file content")}
        mock.return_value = (s3_client, "test_bucket")
        yield mock


@pytest.fixture
def mock_get_data_from_sheet():
    with patch("core.api.v1.catalog.tasks.import_materials_from_xlsx.get_data_from_sheet") as mock:
        mock.return_value = [{"title": "Material 1", "code": "123", "category": "1", "price": 10.99}]
        yield mock


@pytest.fixture
def mock_get_valid_materials():
    with patch("core.api.v1.catalog.tasks.import_materials_from_xlsx.get_valid_materials") as mock:
        mock.return_value = [MagicMock(title="Material 1", code="123", category=1, price=10.99)]
        yield mock


@pytest.fixture
def mock_file():
    file = MagicMock()
    file.name = "test_file.xlsx"
    yield file


@pytest.fixture
def mock_document(mock_file):
    mock = MagicMock(file=mock_file)
    mock.save = MagicMock()
    yield mock


@pytest.fixture
def mock_DocumentModel(mock_document):
    with patch("core.api.v1.catalog.tasks.import_materials_from_xlsx.DocumentModel") as mock:
        mock.objects.get.return_value = mock_document
        yield mock


@pytest.fixture
def mock_MaterialModel():
    with patch("core.api.v1.catalog.tasks.import_materials_from_xlsx.MaterialModel") as mock:
        yield mock


@pytest.mark.django_db
def test_import_materials_from_xls(
    mock_tempfile,
    mock_openpyxl,
    mock_get_s3_data_from_env,
    mock_get_data_from_sheet,
    mock_get_valid_materials,
    mock_document,
    mock_file,
    mock_DocumentModel,
    mock_MaterialModel,
):
    import_materials_from_xls(1)

    mock_get_s3_data_from_env.assert_called_once()
    mock_DocumentModel.objects.get.assert_called_once_with(pk=1)
    mock_document.save.assert_called() == 2
    mock_get_data_from_sheet.assert_called_once()
    mock_get_valid_materials.assert_called_once()
    mock_MaterialModel.objects.bulk_create.assert_called_once()
