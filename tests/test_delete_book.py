import unittest
from unittest.mock import patch, mock_open
import json

from mylib import LibraryManagement


class TestLibraryManagement(unittest.TestCase):
    def setUp(self):
        self.db_file_name = 'test_library.json'
        self.library = LibraryManagement(self.db_file_name)

    @patch('builtins.input', side_effect=['Test Book', 'Test Author', '2021'])
    @patch('builtins.open', new_callable=mock_open)
    def test_add_book(self, mock_file, mock_input):
        with patch('uuid.uuid4', return_value='1'):
            self.library.add_book()

        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0], {
            'id': '1',
            'title': 'Test Book',
            'author': 'Test Author',
            'year': '2021',
            'status': 'в наличии'
        })

        handle = mock_file()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        expected_data = json.dumps(self.library.books, ensure_ascii=False, indent=4)
        self.assertEqual(written_data, expected_data)

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.open', new_callable=mock_open,
           read_data='[{"id": "1", "title": "Test Book", "author": "Test Author", "year": "2021", "status": "в наличии"}]')
    def test_delete_book(self, mock_file, mock_input):
        self.library.load_db()
        self.library.delete_book()

        self.assertEqual(len(self.library.books), 0)

        handle = mock_file()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        expected_data = json.dumps(self.library.books, ensure_ascii=False, indent=4)
        self.assertEqual(written_data, expected_data)


if __name__ == '__main__':
    unittest.main()
