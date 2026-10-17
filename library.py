import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER
);
CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL REFERENCES books(id),
    member_id INTEGER NOT NULL REFERENCES members(id),
    loaned_on TEXT NOT NULL DEFAULT (date('now')),
    returned_on TEXT
);
"""


class Library:
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(SCHEMA)

    def _execute(self, sql, params=()):
        with self.db:
            return self.db.execute(sql, params)

    def _query(self, sql, params=()):
        return [dict(row) for row in self.db.execute(sql, params)]

    def add_book(self, title, author, year=None):
        return self._execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year)
        ).lastrowid

    def add_member(self, name, email):
        return self._execute(
            "INSERT INTO members (name, email) VALUES (?, ?)", (name, email)
        ).lastrowid

    def search_books(self, text=""):
        pattern = f"%{text}%"
        return self._query(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY title",
            (pattern, pattern),
        )

    def available_books(self):
        return self._query(
            "SELECT * FROM books WHERE id NOT IN "
            "(SELECT book_id FROM loans WHERE returned_on IS NULL) ORDER BY title"
        )

    def lend(self, book_id, member_id):
        if self._query("SELECT 1 FROM loans WHERE book_id = ? AND returned_on IS NULL", (book_id,)):
            raise ValueError("Cartea este deja imprumutata")
        return self._execute(
            "INSERT INTO loans (book_id, member_id) VALUES (?, ?)", (book_id, member_id)
        ).lastrowid

    def return_book(self, book_id):
        cursor = self._execute(
            "UPDATE loans SET returned_on = date('now') WHERE book_id = ? AND returned_on IS NULL",
            (book_id,),
        )
        if cursor.rowcount == 0:
            raise ValueError("Cartea nu este imprumutata")

    def active_loans(self):
        return self._query(
            "SELECT b.title, m.name, l.loaned_on FROM loans l "
            "JOIN books b ON b.id = l.book_id JOIN members m ON m.id = l.member_id "
            "WHERE l.returned_on IS NULL ORDER BY l.loaned_on"
        )

    def most_borrowed(self, limit=3):
        return self._query(
            "SELECT b.title, COUNT(*) AS loans FROM loans l JOIN books b ON b.id = l.book_id "
            "GROUP BY b.id ORDER BY loans DESC, b.title LIMIT ?",
            (limit,),
        )
