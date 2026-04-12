from abc import ABC, abstractmethod
from datetime import datetime
from re import fullmatch
from typing import Dict, List, Self
from uuid import UUID, uuid4


class BaseModel(ABC):
    def __init__(self):
        self._id: UUID = uuid4()
        self._created_at: datetime = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def created_at(self):
        return self._created_at

    @abstractmethod
    def to_dict(self) -> Dict[str, str]:
        return {
            "id": str(self._id),
            "created_at": self._created_at.strftime("%d-%m-%Y, %H:%M:%S"),
        }

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, str]) -> Self: ...

    def __eq__(self, other):
        if not isinstance(other, BaseModel):
            return False

        return self._id == other.id

    @abstractmethod
    def __repr__(self):
        return f"BaseClass({self._id!r}, {self._created_at!r})"


class User(BaseModel):
    def __init__(
        self, username: str = "username", email: str = "email@email.com"
    ):
        super().__init__()
        self.username = username
        self.email = email

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str):
        if len(username) < 3:
            raise ValueError("username must be more than 3 charecters")
        self._username = username

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        pattern = r"^[\w\.-]+@[a-zA-Z\d-]+\.[a-zA-Z]{2,}$"
        if fullmatch(pattern, email):
            self._email = email
        else:
            raise ValueError()

    def get_permissions(self) -> List[str]:
        return ["read", "write"]

    def to_dict(self) -> Dict[str, str]:
        return {
            **super().to_dict(),
            "username": self._username,
            "email": self._email,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> Self:
        instance = cls(username=data["username"], email=data["email"])
        instance._id = UUID(data["id"])
        instance._created_at = datetime.strptime(
            data["created_at"], "%d-%m-%Y, %H:%M:%S"
        )
        return instance

    def __repr__(self):
        return (
            f"User({self._id!r}, {self._created_at!r}, "
            f"{self.username!r}, {self.email!r})"
        )


class AdminUser(User):
    def get_permissions(self) -> List[str]:
        return [*super().get_permissions(), "delete", "manage_users"]

    def __repr__(self):
        return (
            f"AdminUser({self._id!r}, {self._created_at!r}, "
            f"{self.username!r}, {self.email!r})"
        )
