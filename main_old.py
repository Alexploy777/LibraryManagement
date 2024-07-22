import json
import os


class LibraryManagement:
    db_file_name = 'library.json'
    def __init__(self):
        if os.path.exists(self.db_file_name):
            print(f'файл базы данных {self.db_file_name} - найден!')
        else:
            print(f'файл базы данных {self.db_file_name} - не найден, создаем новый!')
            self.make_db_start_file()

        print('1 - Добавить книгу', '2 - Удать книгу', '3 - Найти книгу', '4 - Отобразить все книги', '5 - Изменить статус книги', sep='\n')
        action = input('Введите действие: ')
        if action == '1':
            self.add_book()
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


    def read_db_file(self):
        with open(self.db_file_name, "r") as db_file:
            data = json.load(db_file)# чтение из файла базы данных
            return data

    def write_db_file(self, data):
        with open(self.db_file_name, "w", encoding="utf-8") as db_file:
            json.dump(data, db_file)

    def make_db_start_file(self):
        with open(self.db_file_name, "w", encoding="utf-8") as db_file:
            json.dump('', db_file)


    def add_book(self):
        db = self.read_db_file()


        try:
            current_id = [max(int(db.keys()))] + 1
        except:
            print('исключение!')
            current_id: int = 0

        title = input('Введите название книги: ')
        author = input('Введите автора книги: ')
        year = input('Введите год издания книги: ')

        book = {
            'title': title,
            'author': author,
            'year': year,
        }
        self.db = {
            current_id: {'book': book,'status': True},

        }

        print(self.db)
        self.write_db_file(self.db)

    #
    #
    # def remove_book(self, title):
    #     del self.db[title]
    #
    # def get_book(self, title):
    #     return self.db[title]





if __name__ == '__main__':
    lm = LibraryManagement() # создание экземпляра класса

