from models import User
from storage import JsonStorage

if __name__ == "__main__":
    user = User()

    print(user.to_dict())

    storage = JsonStorage("data/db.json")
