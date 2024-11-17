from unittest import mock

from core.api.v1.catalog.tasks.import_materals_from_xlsx import get_data_from_sheet


def test_get_data_from_sheet():
    mock_sheet = mock.Mock()
    mock_sheet.iter_rows.return_value = [
        ("Title 1", "Category A", 1, "Code1", 100),
        ("Title 2", "Category B", 2, "Code2", 200),
    ]

    result = get_data_from_sheet(mock_sheet)

    expected_result = [
        {"title": "Title 1", "category": 1, "code": "Code1", "price": 100},
        {"title": "Title 2", "category": 2, "code": "Code2", "price": 200},
    ]
    assert result == expected_result
    mock_sheet.iter_rows.assert_called_once_with(min_row=2, values_only=True)
