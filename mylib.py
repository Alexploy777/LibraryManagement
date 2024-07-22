import json
import uuid


class LibraryManagement:
    def __init__(self, db_file_name: str):
        self.db_file_name = db_file_name
        self.load_db()

    def load_db(self):
        try:
            with open(self.db_file_name, 'r', encoding='utf-8') as f:
                self.db = json.load(f)
                self.books = [book for book in self.db]
        except FileNotFoundError:
            self.books = []

    def save_db(self):
        with open(self.db_file_name, 'w', encoding='utf-8') as f:
            json.dump([book for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self):
        id = str(uuid.uuid4())
        title = input('Введите название книги: ')
        author = input('Введите автора книги: ')
        year = input('Введите год издания книги: ')
        status = 'в наличии'
        new_book = {
            'id': id, 'title': title, 'author': author, 'year': year, 'status': status,
        }
        self.books.append(new_book)
        self.save_db()
        main()


def main():
    db_file_name = 'library.json'
    lib = LibraryManagement(db_file_name)
    print('1 - Добавить книгу', '2 - Удать книгу', '3 - Найти книгу', '4 - Отобразить все книги',
          '5 - Изменить статус книги', sep='\n')
    action = input('Введите действие: ')
    if action == '1':
        lib.add_book()
    # elif action == '2':
    #     self.delete_book()
    # elif action == '3':
    #     self.find_book()
    # elif action == '4':
    #     self.show_all_books()
    # elif action == '5':
    #     self.change_book_status()
    # else:
    #     print('Неверный ввод!')


if __name__ == '__main__':
    main()
