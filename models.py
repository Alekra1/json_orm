from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Self
from uuid import UUID, uuid4


class BaseModel(ABC):
    def __init__(self):
        _id: UUID = uuid4()
        _created_at: datetime = datetime.now()

    # @property
    # def id(self):
    #     return self._id

    # @id.setter

    @abstractmethod
    def to_dict(self) -> Dict[str, str]: ...

    @abstractmethod
    def from_dict(cls, data: Dict[str, str]) -> Self: ...

    def __eq__(self, other):
        if not isinstance(other, BaseModel):
            return False

        return self.id == other.id
