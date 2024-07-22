import json
import uuid
from typing import List, Dict, Optional


class LibraryManagement:
    def __init__(self, db_file_name: str):
        """
        Инициализация класса управления библиотекой.

        :param db_file_name: Имя файла базы данных
        """
        self.db_file_name: str = db_file_name
        self.books: List[Dict[str, str]] = []
        self.load_db()

    def load_db(self) -> None:
        """
        Загрузка базы данных из файла.
        """
        try:
            with open(self.db_file_name, 'r', encoding='utf-8') as f:
                self.books = json.load(f)
        except FileNotFoundError:
            self.books = []

    def save_db(self) -> None:
        """
        Сохранение базы данных в файл.
        """
        with open(self.db_file_name, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def add_book(self) -> None:
        """
        Добавление новой книги в базу данных.
        """
        id: str = str(uuid.uuid4())
        title: str = input('Введите название книги: ')
        author: str = input('Введите автора книги: ')
        year: str = self.input_year()
        status: str = 'в наличии'
        new_book: Dict[str, str] = {
            'id': id, 'title': title, 'author': author, 'year': year, 'status': status,
        }
        self.books.append(new_book)
        self.save_db()
        print(f'Книга c id {id} успешно добавлена!')
        main()

    def delete_book(self) -> None:
        """
        Удаление книги из базы данных по идентификатору.
        """
        id_book: str = input('Введите идентификатор книги: ').strip()
        book: Optional[Dict[str, str]] = next((b for b in self.books if b['id'] == id_book), None)
        if book:
            self.books.remove(book)
            self.save_db()
            print(f'Книга "{book["title"]}" успешно удалена!')
        else:
            print('Книга с таким идентификатором не найдена!')
        main()

    def find_book(self) -> None:
        """
        Поиск книги в базе данных по названию, автору или году издания.
        """
        search_options: Dict[str, str] = {
            '1': 'title',
            '2': 'author',
            '3': 'year'
        }
        print('1 - Название книги', '2 - Автор книги', '3 - Год издания книги', sep='\n')
        action: str = input('Введите метод поиска: ').strip()
        if action in search_options:
            if search_options[action] == 'year':
                query: str = self.input_year()
            else:
                query = input(f'Введите {search_options[action]} книги: ').strip().lower()
            found_books: List[Dict[str, str]] = [book for book in self.books if query in book[search_options[action]].lower()]
            if found_books:
                for book in found_books:
                    print(f'Найдена книга id: {book["id"]}, название: {book["title"]}, автор: {book["author"]}, год: {book["year"]}, статус: {book["status"]}')
            else:
                print(f'Книга с таким {search_options[action]} не найдена!')
        else:
            print('Неверный ввод!')
        main()

    def show_all_books(self) -> None:
        """
        Отображение всех книг в базе данных.
        """
        for book in self.books:
            print(
                f'id: {book["id"]}, название: {book["title"]}, автор: {book["author"]}, год: {book["year"]}, статус: {book["status"]}'
            )
        main()

    def change_book_status(self) -> None:
        """
        Изменение статуса книги по идентификатору.
        """
        id_book: str = input('Введите идентификатор книги: ').strip()
        book: Optional[Dict[str, str]] = next((b for b in self.books if b['id'] == id_book), None)
        if book:
            print('1 - в наличии', '2 - выдана', sep='\n')
            new_status: str = input('Введите статус книги: ').strip()
            if new_status == '1':
                book['status'] = 'в наличии'
            elif new_status == '2':
                book['status'] = 'выдана'
            else:
                print('Неверный ввод!')
                return main()
            self.save_db()
            print(f'Статус книги "{book["title"]}" изменен на "{book["status"]}"')
        else:
            print('Книга с таким идентификатором не найдена!')
        main()

    def input_year(self) -> str:
        """
        Проверка правильности ввода года.

        :return: Год издания книги
        """
        while True:
            year: str = input('Введите год издания книги: ').strip()
            if year.isdigit() and len(year) == 4:
                return year
            print('Неверный ввод! Год издания должен быть числом из 4 цифр.')


def main() -> None:
    """
    Основное меню приложения.
    """
    db_file_name: str = 'library.json'
    lib: LibraryManagement = LibraryManagement(db_file_name)
    print('1 - Добавить книгу', '2 - Удалить книгу', '3 - Найти книгу', '4 - Отобразить все книги',
          '5 - Изменить статус книги', sep='\n')
    action: str = input('Введите действие: ')
    if action == '1':
        lib.add_book()
    elif action == '2':
        lib.delete_book()
    elif action == '3':
        lib.find_book()
    elif action == '4':
        lib.show_all_books()
    elif action == '5':
        lib.change_book_status()
    else:
        print('Неверный ввод!')


if __name__ == '__main__':
    main()
