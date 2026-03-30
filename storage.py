from pathlib import Path


class JsonStorage:
    def __init__(self, file_path: str):
        self.file_path = file_path

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path: str):
        try:
            self._file_path = Path(file_path)
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid path: {file_path}") from e
