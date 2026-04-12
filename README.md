# JSON ORM

A simple ORM simulator written in Python. It maps Python objects to JSON and supports CRUD operations, filtering, sorting, and aggregation. All data is stored in a single JSON file that acts as the database.

## Class Structure

**`BaseModel` (abstract)** — Base for all models. Holds `id` (UUID, auto-generated) and `created_at` (timestamp). Defines the `to_dict` / `from_dict` interface and the `__eq__` operator.

**`User(BaseModel)`** — A regular user. Adds `username` (min 3 chars) and `email` (validated against a regex pattern). Implements `get_permissions()` returning `["read", "write"]`.

**`AdminUser(User)`** — Extends `User` with no extra fields. Overrides `get_permissions()` to also return `"delete"` and `"manage_users"`.

## Special Functions

**`__eq__` (operator overload)** — Two model instances are equal if and only if their `id` fields match. This means two separate objects with the same UUID are treated as the same record.

**`get_permissions()` (polymorphism)** — `User` returns `["read", "write"]`; `AdminUser` calls `super()` and appends `["delete", "manage_users"]`. Same method name, different output depending on the class.

**Data manipulation methods** — `filter_by(field, value)` returns records where a field matches a value; `sort_by(field, reverse)` returns all records sorted by a field; `count()` and `count_where(field, value)` return record counts.

## How to Run

Run the program:
```
python main.py --db data/db.json
```

Run tests:
```
uv run coverage run -m unittest discover
```

Generate coverage report:
```
uv run coverage report
```

## Docstring Format

This project uses Google-style docstrings.
