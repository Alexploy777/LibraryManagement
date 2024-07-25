import unittest
from unittest.mock import mock_open, patch
import json
from mylib import LibraryManagement

class TestLibraryManagement(unittest.TestCase):
    def setUp(self):
        self.db_file_name = 'test_library.json'
        self.library = LibraryManagement(self.db_file_name)

    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_load_db(self, mock_file):
        self.library.load_db()
        self.assertEqual(self.library.books, [])
        mock_file.assert_called_with(self.db_file_name, 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_save_db(self, mock_file):
        self.library.books = [{'id': '1', 'title': 'Test Book', 'author': 'Test Author', 'year': '2021', 'status': 'в наличии'}]
        self.library.save_db()
        mock_file.assert_called_with(self.db_file_name, 'w', encoding='utf-8')
        handle = mock_file()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        expected_data = json.dumps(self.library.books, ensure_ascii=False, indent=4)
        self.assertEqual(written_data, expected_data)

if __name__ == '__main__':
    unittest.main()
