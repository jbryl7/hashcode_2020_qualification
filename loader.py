from library import Library


class Loader:
    def __init__(self, data_set_name):
        self.data_set_name = data_set_name

        self.n_books = 0
        self.n_libraries = 0
        self.n_days = 0

        self.libraries = []
        self.book_scores = []
        self.selected_libraries = []
        self.is_book_id_selected = []
        self.selected_libraries_with_book = []

        self.load_data_set()

    def load_data_set(self):
        input_filename = "data/" + self.data_set_name + ".txt"

        with open(input_filename) as file:
            def get_int_list_from_line():
                return [int(x) for x in file.readline().split()]

            self.n_books, self.n_libraries, self.n_days = get_int_list_from_line()
            self.book_scores = get_int_list_from_line()

            for lib_id in range(self.n_libraries):
                lib_n_books, lib_signup_time, lib_books_per_day = get_int_list_from_line()
                lib_books = get_int_list_from_line()

                library = Library(lib_id, lib_n_books, lib_signup_time, lib_books_per_day, lib_books)
                self.libraries.append(library)

        self.selected_libraries = []
        self.is_book_id_selected = [False] * self.n_books

    def get_data_summary(self):
        return {
            "data_set": self.data_set_name,
            "n_libraries": self.n_libraries,
            "n_books": self.n_books,
            "n_days": self.n_days
        }
