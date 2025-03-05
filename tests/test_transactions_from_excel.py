import unittest
from unittest.mock import patch, MagicMock
from src.transactions_from_excel import load_transactions_from_excel


class TestLoadTransactionsFromExcel(unittest.TestCase):

    @patch('openpyxl.load_workbook')
    def test_load_transactions_file_not_found(self, mock_load_workbook: MagicMock) -> None:
        mock_load_workbook.side_effect = FileNotFoundError("File not found")
        with self.assertRaises(FileNotFoundError):
            load_transactions_from_excel('dummy_path.xlsx')

    @patch('openpyxl.load_workbook')
    def test_load_transactions_general_exception(self, mock_load_workbook: MagicMock) -> None:
        mock_load_workbook.side_effect = Exception("General error")
        with self.assertRaises(Exception):
            load_transactions_from_excel('dummy_path.xlsx')

    @patch('openpyxl.load_workbook')
    def test_load_transactions_incorrect_row_length(self, mock_load_workbook: MagicMock) -> None:
        mock_sheet = MagicMock()
        header_cells = [
            MagicMock(value='ID'),
            MagicMock(value='Description'),
            MagicMock(value='Amount'),
            MagicMock(value='Currency')
        ]
        mock_sheet.__getitem__.return_value = header_cells
        mock_sheet.iter_rows.return_value = [
            (1, 'Transaction 1', 100, 'USD'),
            (2, 'Transaction 2', 200)
        ]

        mock_workbook = MagicMock()
        mock_workbook.active = mock_sheet
        mock_workbook.sheetnames = ['Sheet1']
        mock_load_workbook.return_value = mock_workbook

        transactions = load_transactions_from_excel('dummy_path.xlsx')
        self.assertEqual(len(transactions), 1)

    @patch('openpyxl.load_workbook')
    def test_load_transactions_no_sheets(self, mock_load_workbook: MagicMock) -> None:
        mock_workbook = MagicMock()
        mock_workbook.sheetnames = []
        mock_load_workbook.return_value = mock_workbook

        with self.assertRaises(ValueError):
            load_transactions_from_excel('dummy_path.xlsx')

    @patch('openpyxl.load_workbook')
    def test_load_transactions_success(self, mock_load_workbook: MagicMock) -> None:
        mock_sheet = MagicMock()
        header_cells = [
            MagicMock(value='ID'),
            MagicMock(value='Description'),
            MagicMock(value='Amount'),
            MagicMock(value='Currency')
        ]
        mock_sheet.__getitem__.return_value = header_cells
        mock_sheet.iter_rows.return_value = [
            (1, 'Transaction 1', 100, 'USD'),
            (2, 'Transaction 2', 200, 'EUR')
        ]

        mock_workbook = MagicMock()
        mock_workbook.active = mock_sheet
        mock_workbook.sheetnames = ['Sheet1']
        mock_load_workbook.return_value = mock_workbook

        transactions = load_transactions_from_excel('dummy_path.xlsx')
        self.assertEqual(len(transactions), 2)


if __name__ == '__main__':
    unittest.main()
