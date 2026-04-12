# ORM class that provides CRUD, filtering, sorting, and counting operations.
from operator import itemgetter
from typing import List
from uuid import UUID

from models import User
from storage import JsonStorage


class ORM:
    """Simple ORM that maps User objects to a JSON storage backend.

    Args:
        storage: A configured ``JsonStorage`` instance with a file path set.
    """

    def __init__(self, storage: JsonStorage):
        self.storage = storage

    @property
    def storage(self):
        return self._storage

    @storage.setter
    def storage(self, storage: JsonStorage):
        if not isinstance(storage, JsonStorage):
            raise ValueError(f"Invalid storage: {storage}")
        if not storage.file_path:
            raise ValueError(
                "You must provide the storage with specified storage file"
            )
        self._storage = storage

    def create(self, model: User):
        """Append a new record to storage."""
        dictionary_model = model.to_dict()
        data = self.storage.load()
        data.append(dictionary_model)
        self.storage.save(data)

    def get_all(self) -> List[User]:
        """Return all records as User instances."""
        data = self.storage.load()
        models = []
        for model in data:
            models.append(User.from_dict(model))
        return models

    def get_by_id(self, id: UUID) -> User | None:
        """Return the record matching ``id``, or ``None`` if not found."""
        data = self.storage.load()
        for record in data:
            if record["id"] == str(id):
                return User.from_dict(record)
        return None

    def update(self, id: UUID, updated_record: User):
        """Overwrite non-protected fields of the record with ``id``."""
        data = self.storage.load()
        updated_dictionary = updated_record.to_dict()
        protected_fields = {"id", "created_at"}
        for record in data:
            if record["id"] == str(id):
                for key, value in updated_dictionary.items():
                    if key not in protected_fields:
                        record[key] = value
                break
        self.storage.save(data)

    def delete(self, id: UUID):
        """Remove the record with ``id`` from storage."""
        data = self.storage.load()
        for record in data:
            if record["id"] == str(id):
                data.remove(record)
                break
        self.storage.save(data)

    def filter_by(self, field: str, value: str) -> List[User]:
        """Return raw dicts where ``field`` equals ``value``."""
        data = self.storage.load()
        filtered_list = []
        for record in data:
            if record[field] == value:
                filtered_list.append(record)
        return filtered_list

    def sort_by(self, field: str, reverse: bool = False) -> List[User]:
        """Return all records sorted by ``field``.

        Args:
            field: Record key to sort on.
            reverse: If ``True``, sort descending.
        """
        data = self.storage.load()
        sorted_data = sorted(data, key=itemgetter(field), reverse=reverse)
        return [User.from_dict(record) for record in sorted_data]

    def count(self) -> int:
        """Return the total number of records."""
        return len(self.storage.load())

    def count_where(self, field: str, value: str) -> int:
        """Return the number of records where ``field`` equals ``value``."""
        return len(self.filter_by(field, value))
