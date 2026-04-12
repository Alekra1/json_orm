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

### Using uv (Recommended)

This project is recommended to be run using `uv` (a fast Python package manager).

To run the program:
```
uv run main.py --db data/db.json
```

To run tests:
```
uv run python -m unittest
```

To generate a coverage report:
```
uv run coverage run -m unittest && uv run coverage report
```

### Without uv (Standard Python)

You can also run the project without `uv`, but you need to install the required packages from `pyproject.toml` first.

Install dependencies (it's recommended to use a virtual environment):
```
pip install .
```
Or install them manually: `pip install coverage flake8`

Run the program:
```
python main.py --db data/db.json
```

Run tests:
```
python -m unittest
```

Generate coverage report:
```
coverage run -m unittest && coverage report
```

## Docstring Format

This project uses Google-style docstrings.
