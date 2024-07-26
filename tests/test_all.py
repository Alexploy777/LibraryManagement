import unittest
from unittest.mock import patch, mock_open
import json

from mylib import LibraryManagement


class TestLibraryManagement(unittest.TestCase):
    def setUp(self):
        self.db_file_name = 'test_library.json'
        self.library = LibraryManagement(self.db_file_name)

    @patch('builtins.input', side_effect=['Test Book', 'Test Author',  'not_a_year', '2021'])
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

    @patch('builtins.input', side_effect=['1', 'Test Book'])
    @patch('builtins.open', new_callable=mock_open,
           read_data='[{"id": "1", "title": "Test Book", "author": "Test Author", "year": "2021", "status": "в наличии"}]')
    def test_find_book(self, mock_file, mock_input):
        self.library.load_db()
        with patch('builtins.print') as mock_print:
            self.library.find_book()
            # Проверяем вызовы print с несколькими аргументами
            mock_print.assert_any_call('1 - Название книги', '2 - Автор книги', '3 - Год издания книги', sep='\n')
            mock_print.assert_any_call(
                'Найдена книга id: 1, название: Test Book, автор: Test Author, год: 2021, статус: в наличии')

    @patch('builtins.open', new_callable=mock_open,
           read_data='[{"id": "1", "title": "Test Book", "author": "Test Author", "year": "2021", "status": "в наличии"}]')
    def test_show_all_books(self, mock_file):
        self.library.load_db()
        with patch('builtins.print') as mock_print:
            self.library.show_all_books()
            mock_print.assert_any_call('id: 1, название: Test Book, автор: Test Author, год: 2021, статус: в наличии')

    @patch('builtins.input', side_effect=['1', '2'])
    @patch('builtins.open', new_callable=mock_open,
           read_data='[{"id": "1", "title": "Test Book", "author": "Test Author", "year": "2021", "status": "в наличии"}]')
    def test_change_book_status(self, mock_file, mock_input):
        self.library.load_db()
        self.library.change_book_status()

        self.assertEqual(self.library.books[0]['status'], 'выдана')

        handle = mock_file()
        written_data = ''.join(call.args[0] for call in handle.write.call_args_list)
        expected_data = json.dumps(self.library.books, ensure_ascii=False, indent=4)
        self.assertEqual(written_data, expected_data)

    @patch('builtins.open', new_callable=mock_open,
           read_data='[{"id": "1", "title": "Test Book", "author": "Test Author", "year": "2021", "status": "в наличии"}]')
    def test_load_db(self, mock_file):
        self.library.load_db()
        self.assertEqual(self.library.books, [
            {"id": "1", "title": "Test Book", "author": "Test Author", "year": "2021", "status": "в наличии"}])


if __name__ == '__main__':
    unittest.main()
