import argparse
import sqlite3

from library import Library


def print_rows(rows):
    if not rows:
        print("Nu exista inregistrari.")
    for row in rows:
        print(" | ".join(str(value) for value in row.values()))


def build_parser():
    parser = argparse.ArgumentParser(description="Gestiunea unei biblioteci")
    parser.add_argument("--db", default="biblioteca.db", help="fisierul bazei de date")
    commands = parser.add_subparsers(dest="command", required=True)

    book = commands.add_parser("add-book", help="adauga o carte")
    book.add_argument("title")
    book.add_argument("author")
    book.add_argument("year", type=int, nargs="?")

    member = commands.add_parser("add-member", help="adauga un cititor")
    member.add_argument("name")
    member.add_argument("email")

    search = commands.add_parser("books", help="cauta carti dupa titlu sau autor")
    search.add_argument("text", nargs="?", default="")

    commands.add_parser("available", help="cartile disponibile")

    lend = commands.add_parser("lend", help="imprumuta o carte")
    lend.add_argument("book_id", type=int)
    lend.add_argument("member_id", type=int)

    give_back = commands.add_parser("return", help="returneaza o carte")
    give_back.add_argument("book_id", type=int)

    commands.add_parser("loans", help="imprumuturile active")
    commands.add_parser("top", help="cele mai imprumutate carti")
    return parser


def run(library, args):
    actions = {
        "add-book": lambda: print("Carte adaugata cu id", library.add_book(args.title, args.author, args.year)),
        "add-member": lambda: print("Cititor adaugat cu id", library.add_member(args.name, args.email)),
        "books": lambda: print_rows(library.search_books(args.text)),
        "available": lambda: print_rows(library.available_books()),
        "lend": lambda: print("Imprumut inregistrat cu id", library.lend(args.book_id, args.member_id)),
        "return": lambda: (library.return_book(args.book_id), print("Carte returnata")),
        "loans": lambda: print_rows(library.active_loans()),
        "top": lambda: print_rows(library.most_borrowed()),
    }
    actions[args.command]()


def main():
    args = build_parser().parse_args()
    try:
        run(Library(args.db), args)
    except (ValueError, sqlite3.IntegrityError) as error:
        print("Eroare:", error)


if __name__ == "__main__":
    main()
