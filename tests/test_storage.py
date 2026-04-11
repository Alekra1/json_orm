import tempfile
import unittest
from pathlib import Path
from uuid import uuid4

import storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)
        self.addCleanup(self.temp_dir.cleanup)

    def test_default_path(self):
        json_storage = storage.JsonStorage()

        expected_default_path = "data/db.json"

        self.assertEqual(str(json_storage.file_path), expected_default_path)

    def test_round_trip(self):
        test_storage_file = self.tmp_path / "test.json"
        json_storage = storage.JsonStorage(str(test_storage_file))

        test_data = [
            {
                "id": str(uuid4()),
                "username": "alice_smith",
                "email": "alice@example.com",
                "role": "admin",
            },
            {
                "id": str(uuid4()),
                "username": "bob_jones",
                "email": "bob@example.com",
                "role": "user",
            },
            {
                "id": str(uuid4()),
                "username": "charlie_brown",
                "email": "charlie@example.com",
                "role": "moderator",
            },
        ]

        json_storage.save(test_data)

        loaded_data = json_storage.load()

        self.assertEqual(test_data, loaded_data)

    def test_non_existing_file(self):
        non_existent_path = self.tmp_path / "does_not_exist.json"
        json_storage = storage.JsonStorage(str(non_existent_path))
        self.assertEqual(json_storage.load(), [])

    def test_non_serializable_json(self):
        test_storage_file = self.tmp_path / "test.json"
        json_storage = storage.JsonStorage(str(test_storage_file))

        test_data = [
            {
                "id": str(uuid4()),
                "username": "alice_smith",
                "email": "alice@example.com",
                "role": "admin",
                "invalid_field": {
                    "this",
                    "is",
                    "a",
                    "set",
                },  # Sets are not JSON serializable
            }
        ]

        with self.assertRaises(ValueError):
            json_storage.save(test_data)

    def test_invalid_json_load(self):
        test_storage_file = self.tmp_path / "test.json"
        json_storage = storage.JsonStorage(str(test_storage_file))
        malformed_json_string = '[{"id": "1", "name": "Alice"'
        with open(test_storage_file, "w") as f:
            f.write(malformed_json_string)

        with self.assertRaises(ValueError) as context:
            json_storage.load()

        self.assertTrue("Invalid JSON:" in str(context.exception))

    def test_init_with_directory_path(self):
        with self.assertRaises(IsADirectoryError):
            storage.JsonStorage(str(self.tmp_path))

    def test_init_with_invalid_path_type(self):
        with self.assertRaises(ValueError):
            storage.JsonStorage(12345)


if __name__ == "__main__":
    unittest.main()
