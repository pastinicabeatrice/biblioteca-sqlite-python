import sqlite3
import unittest

from library import Library


class LibraryTest(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.ion = self.library.add_book("Ion", "Liviu Rebreanu", 1920)
        self.enigma = self.library.add_book("Enigma Otiliei", "George Calinescu", 1938)
        self.ana = self.library.add_member("Ana Pop", "ana@example.com")

    def titles(self, rows):
        return [row["title"] for row in rows]

    def test_search_by_title_or_author(self):
        self.assertEqual(self.titles(self.library.search_books("Rebreanu")), ["Ion"])
        self.assertEqual(self.titles(self.library.search_books("enigma")), ["Enigma Otiliei"])

    def test_lent_book_is_not_available(self):
        self.library.lend(self.ion, self.ana)
        self.assertEqual(self.titles(self.library.available_books()), ["Enigma Otiliei"])
        self.assertEqual(self.library.active_loans()[0]["name"], "Ana Pop")

    def test_book_cannot_be_lent_twice(self):
        self.library.lend(self.ion, self.ana)
        with self.assertRaises(ValueError):
            self.library.lend(self.ion, self.ana)

    def test_returned_book_is_available_again(self):
        self.library.lend(self.ion, self.ana)
        self.library.return_book(self.ion)
        self.assertEqual(len(self.library.available_books()), 2)
        self.assertEqual(self.library.active_loans(), [])

    def test_return_book_that_is_not_lent(self):
        with self.assertRaises(ValueError):
            self.library.return_book(self.ion)

    def test_most_borrowed(self):
        for _ in range(2):
            self.library.lend(self.ion, self.ana)
            self.library.return_book(self.ion)
        self.library.lend(self.enigma, self.ana)
        self.assertEqual(
            self.library.most_borrowed(),
            [{"title": "Ion", "loans": 2}, {"title": "Enigma Otiliei", "loans": 1}],
        )

    def test_email_must_be_unique(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.library.add_member("Alt nume", "ana@example.com")

    def test_lend_requires_existing_member(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.library.lend(self.ion, 999)


if __name__ == "__main__":
    unittest.main()
