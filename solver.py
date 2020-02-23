from tqdm import tqdm
from loader import Loader


class Solver(Loader):
    def __init__(self, data_set_name):
        Loader.__init__(self, data_set_name)

    def solve(self):
        print(self.get_data_summary())

        self.select_libraries()
        self.optimize()
        self.write_to_file()

    def select_libraries(self):
        for library in self.libraries:
            library.books.sort(key=lambda b: self.book_scores[b], reverse=True)

        time_left = self.n_days
        sorted_libraries = self.libraries
        libraries_score_changed = True

        print("library selection progress bar:")
        for _ in tqdm(range(len(self.libraries))):
            if time_left <= 0 or len(sorted_libraries) == 0:
                break

            if libraries_score_changed:
                for library in sorted_libraries:
                    self.calculate_current_library_score(library, time_left)

            sorted_libraries = sorted(sorted_libraries, key=lambda l: l.current_score)
            selected_library = sorted_libraries.pop()

            if time_left - selected_library.signup_time <= 0 or selected_library.current_n_available_books <= 0:
                libraries_score_changed = False
                continue
            time_left -= selected_library.signup_time

            self.selected_libraries.append(selected_library)

            for book_id in selected_library.books:
                if selected_library.current_n_available_books <= 0:
                    break
                if not self.is_book_id_selected[book_id]:
                    selected_library.selected_books.append(book_id)
                    selected_library.current_n_available_books -= 1
                    self.is_book_id_selected[book_id] = True

            libraries_score_changed = True

    def calculate_current_library_score(self, library, time_left):
        max_n_available_books = (time_left - library.signup_time) * library.books_per_day

        available_books_score = 0
        n_scored_books = 0
        for book_id in library.books:
            if not self.is_book_id_selected[book_id] and n_scored_books < max_n_available_books:
                available_books_score += self.book_scores[book_id]
                n_scored_books += 1

        library.current_score = available_books_score / library.signup_time
        library.current_n_available_books = n_scored_books

    def optimize(self):
        for _ in range(self.n_books):
            self.selected_libraries_with_book.append([])

        for lib in self.selected_libraries:
            for book_id in lib.books:
                self.selected_libraries_with_book[book_id].append(lib)

        print("book selection optimization progress bar:")
        for _ in tqdm(range(10)):
            self.optimize_book_selection()

    def optimize_book_selection(self):
        for library1 in self.selected_libraries:
            for common_book_number in range(len(library1.selected_books)):
                common_book_id = library1.selected_books[common_book_number]

                for library2 in self.selected_libraries_with_book[common_book_id]:
                    if library1.id == library2.id:
                        continue

                    library1_best_not_selected_book_number = self.find_best_not_selected_book_number(library1)
                    if library1_best_not_selected_book_number is None:
                        continue
                    library2_worst_selected_book_number = self.find_worst_selected_book_number(library2)

                    library1_best_not_selected_book_id = library1.books[library1_best_not_selected_book_number]
                    library2_worst_selected_book_id = library2.selected_books[library2_worst_selected_book_number]

                    library1_best_not_selected_book_score = self.book_scores[library1_best_not_selected_book_id]
                    library2_worst_selected_book_score = self.book_scores[library2_worst_selected_book_id]

                    if library1_best_not_selected_book_score > library2_worst_selected_book_score:
                        library2.selected_books.pop(library2_worst_selected_book_number)
                        library2.selected_books.append(common_book_id)

                        library1.selected_books[common_book_number] = library1_best_not_selected_book_id

                        self.is_book_id_selected[library1_best_not_selected_book_id] = True
                        self.is_book_id_selected[library2_worst_selected_book_id] = False
                        break

    def find_best_not_selected_book_number(self, library):
        best_not_selected_book_number = None

        for book_number, book_id in enumerate(library.books):
            if not self.is_book_id_selected[book_id]:
                best_not_selected_book_number = book_number
                break

        return best_not_selected_book_number

    def find_worst_selected_book_number(self, library):
        worst_selected_book_number = None
        minimum_selected_book_score = self.book_scores[library.selected_books[0]] + 1

        for book_number, book_id in enumerate(library.selected_books):
            if minimum_selected_book_score > self.book_scores[book_id]:
                worst_selected_book_number = book_number
                minimum_selected_book_score = self.book_scores[book_id]

        return worst_selected_book_number

    def write_to_file(self):
        output_filename = "results/" + self.data_set_name + ".out"

        with open(output_filename, "w+") as file:
            file.write(str(len(self.selected_libraries)) + "\n")
            for library in self.selected_libraries:
                file.write(str(library.id) + " " + str(len(library.selected_books)) + "\n")
                for book_id in library.selected_books:
                    file.write(str(book_id) + " ")
                file.write("\n")

        print("done writing to file " + output_filename + "\n")


if __name__ == '__main__':
    data_set_names = [
        'a_example',
        'b_read_on',
        'c_incunabula',
        'd_tough_choices',
        'e_so_many_books',
        'f_libraries_of_the_world'
    ]

    for data_set_name in data_set_names:
        Solver(data_set_name).solve()
