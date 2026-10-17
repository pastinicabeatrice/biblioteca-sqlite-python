# Bibliotecă - SQLite

Aplicație în linie de comandă pentru gestiunea unei biblioteci, cu bază de date SQLite.

## Funcționalități

- adăugarea cărților și a cititorilor
- căutarea cărților după titlu sau autor
- împrumutarea și returnarea cărților; o carte nu poate fi împrumutată de două ori în același timp
- lista cărților disponibile și a împrumuturilor active
- topul celor mai împrumutate cărți

## Baza de date

| Tabel | Coloane |
|---|---|
| `books` | id, title, author, year |
| `members` | id, name, email (unic) |
| `loans` | id, book_id → books, member_id → members, loaned_on, returned_on |

Interogările folosesc `JOIN`, `GROUP BY`, subinterogări și parametri (fără concatenare de șiruri, deci fără risc de SQL injection).

## Rulare

Necesită Python 3.8 sau mai nou; `sqlite3` face parte din biblioteca standard.

```
python main.py add-book "Ion" "Liviu Rebreanu" 1920
python main.py add-member "Ana Pop" ana@example.com
python main.py lend 1 1
python main.py loans
python main.py return 1
python main.py available
python main.py top
python main.py --help
```

Datele sunt salvate în `biblioteca.db` (altă cale cu `--db`).

Teste:

```
python -m unittest
```
