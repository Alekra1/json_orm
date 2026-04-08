import argparse

from models import User
from orm import ORM
from storage import JsonStorage

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-db", help="specify storage file")
    args = parser.parse_args()
    storage = JsonStorage(args.db)
    orm = ORM(storage)
    user = User()
    orm.create(user)
    print(orm.count())
