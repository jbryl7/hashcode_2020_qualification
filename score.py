from loader import Loader


class Score(Loader):
    def __init__(self, data_set_name):
        Loader.__init__(self, data_set_name)

    def get_score(self):
        all_selected_books = set()
        time_left = self.n_days
        score = 0

        output_filename = "results/" + self.data_set_name + ".out"

        with open(output_filename) as file:
            def get_int_list_from_line():
                return [int(x) for x in file.readline().split()]

            n_selected_libraries = int(file.readline())
            for _ in range(n_selected_libraries):
                selected_library_id, n_selected_books = get_int_list_from_line()
                selected_library = self.libraries[selected_library_id]
                time_left -= selected_library.signup_time

                if not n_selected_books:
                    raise RuntimeError("Library with id=" + str(selected_library_id) + " has no selected books.")
                if n_selected_books > time_left * selected_library.books_per_day:
                    raise RuntimeError("Library with id=" + str(selected_library_id) + " could not have sent " + str(
                        n_selected_books) + " books.")

                selected_books = get_int_list_from_line()
                for book_id in selected_books:
                    all_selected_books.add(book_id)

        for book_id in all_selected_books:
            score += self.book_scores[book_id]

        return score


if __name__ == '__main__':
    data_set_names = [
        'a_example',
        'b_read_on',
        'c_incunabula',
        'd_tough_choices',
        'e_so_many_books',
        'f_libraries_of_the_world'
    ]

    full_score = 0
    for data_set_name in data_set_names:
        score = Score(data_set_name).get_score()
        print(data_set_name + " score is " + str(score))
        full_score += score

    print("\nFull score is " + str(full_score))
