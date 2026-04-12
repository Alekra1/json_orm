import argparse
import os
from uuid import UUID

from models import AdminUser, User
from orm import ORM
from storage import JsonStorage


def clear():
    os.system("clear")


def pause():
    input("\nPress Enter to go back...")
    clear()


MENU = """
1.  Add user
2.  Add admin user
3.  List all records
4.  Get record by ID
5.  Update a record
6.  Delete a record
7.  Filter records
8.  Sort records
9.  Count records
10. Exit
"""


def print_record(record):
    print(f"  ID:         {record.id}")
    print(f"  Type:       {type(record).__name__}")
    print(f"  Username:   {record.username}")
    print(f"  Email:      {record.email}")
    print(f"  Created at: {record.created_at}")


def parse_uuid(raw):
    try:
        return UUID(raw)
    except ValueError:
        print("Invalid ID format.")
        return None


def handle_add_user(orm):
    username = input("Username: ")
    email = input("Email: ")
    try:
        user = User(username=username, email=email)
        orm.create(user)
        print(f"User created with ID: {user.id}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_add_admin(orm):
    username = input("Username: ")
    email = input("Email: ")
    try:
        user = AdminUser(username=username, email=email)
        orm.create(user)
        print(f"Admin user created with ID: {user.id}")
    except ValueError as e:
        print(f"Error: {e}")


def handle_list_all(orm):
    records = orm.get_all()
    clear()
    if not records:
        print("No records found.")
    else:
        for record in records:
            print_record(record)
            print()
    pause()


def handle_get_by_id(orm):
    record_id = parse_uuid(input("Record ID: "))
    if record_id is None:
        return
    record = orm.get_by_id(record_id)
    clear()
    if record is None:
        print("Record not found.")
    else:
        print_record(record)
    pause()


def handle_update(orm):
    record_id = parse_uuid(input("Record ID: "))
    if record_id is None:
        return
    record = orm.get_by_id(record_id)
    if record is None:
        print("Record not found.")
        return
    print(f"Current username: {record.username}")
    print(f"Current email:    {record.email}")
    new_username = input("New username (Enter to keep): ").strip()
    new_email = input("New email (Enter to keep): ").strip()
    try:
        if new_username:
            record.username = new_username
        if new_email:
            record.email = new_email
        orm.update(record_id, record)
        print("Record updated.")
    except ValueError as e:
        print(f"Error: {e}")


def handle_delete(orm):
    record_id = parse_uuid(input("Record ID: "))
    if record_id is None:
        return
    if orm.get_by_id(record_id) is None:
        print("Record not found.")
        return
    orm.delete(record_id)
    print("Record deleted.")


def handle_filter(orm):
    field = input("Field name (e.g. username, email): ")
    value = input("Value: ")
    try:
        results = orm.filter_by(field, value)
    except KeyError:
        print(f"Field '{field}' not found in records.")
        return
    clear()
    if not results:
        print("No matching records.")
    else:
        for record in results:
            print(f"  ID:       {record.get('id')}")
            print(f"  Username: {record.get('username')}")
            print(f"  Email:    {record.get('email')}")
            print()
    pause()


def handle_sort(orm):
    field = input("Field name to sort by (e.g. username, email, created_at): ")
    order = input("Order [asc/desc] (default: asc): ").strip().lower()
    reverse = order == "desc"
    try:
        results = orm.sort_by(field, reverse=reverse)
    except KeyError:
        print(f"Field '{field}' not found in records.")
        return
    clear()
    if not results:
        print("No records.")
    else:
        for record in results:
            print_record(record)
            print()
    pause()


def handle_count(orm):
    total = orm.count()
    answer = input("Count with a condition? [y/n]: ").strip().lower()
    clear()
    print(f"Total records: {total}")
    if answer == "y":
        field = input("Field: ")
        value = input("Value: ")
        try:
            count = orm.count_where(field, value)
            print(f"Records where {field}={value!r}: {count}")
        except KeyError:
            print(f"Field '{field}' not found.")
    pause()


HANDLERS = {
    1: handle_add_user,
    2: handle_add_admin,
    3: handle_list_all,
    4: handle_get_by_id,
    5: handle_update,
    6: handle_delete,
    7: handle_filter,
    8: handle_sort,
    9: handle_count,
}


def run(orm):
    while True:
        print(MENU)
        try:
            choice = int(input("Enter option: "))
        except ValueError:
            print("Please enter a number.")
            continue

        if choice == 10:
            print("Goodbye!")
            break

        handler = HANDLERS.get(choice)
        if handler is None:
            print("Invalid option, try again.")
            continue

        handler(orm)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSON ORM CLI")
    parser.add_argument(
        "--db", required=True, help="Path to the JSON database file"
    )
    args = parser.parse_args()
    storage = JsonStorage(args.db)
    orm = ORM(storage)
    run(orm)
