from models import BaseModel
from storage import JsonStorage


class ORM:
    def __init__(self, storage: JsonStorage):
        self.storage = storage

    @property
    def storage(self):
        return self.storage

    @storage.setter
    def storage(self, storage: JsonStorage):
        if storage is not isinstance(storage, JsonStorage):
            raise ValueError(f"Invalid storage: {storage}")
        self._storage = storage

    def create(self, model: BaseModel):
        self.storage.load()
