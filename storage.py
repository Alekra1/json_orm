# Handles saving and loading data to/from a JSON file.
import json
from pathlib import Path
from typing import Dict, List


class JsonStorage:
    """Persists a list of records to a JSON file.

    Args:
        file_path: Path to the JSON file. Defaults to ``data/db.json``.
    """

    def __init__(self, file_path: str | None = None):
        if not file_path:
            self.file_path = "data/db.json"
        else:
            self.file_path = file_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        try:
            p = Path(file_path)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid path: {file_path}") from e
        if p.is_dir():
            raise IsADirectoryError(f"{p} is a directory")
        self._file_path = p

    def load(self) -> List[Dict[str, str]]:
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def save(self, data: List[Dict[str, str]]):
        try:
            with open(self._file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except TypeError as e:
            raise ValueError(f"Data is not JSON serializable: {e}") from e
        except OSError as e:
            raise OSError(f"Failed to write file: {e}") from e
