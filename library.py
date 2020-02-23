class Library:
    def __init__(self, lib_id, n_books, signup_time, books_per_day, books):
        self.id = lib_id

        self.n_books = n_books
        self.signup_time = signup_time
        self.books_per_day = books_per_day
        self.books = books
        self.selected_books = []

        self.current_score = 0
        self.current_n_available_books = 0
