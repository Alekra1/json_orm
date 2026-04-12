# Unit tests for the ORM class.
import tempfile
import unittest
import uuid
from pathlib import Path

import orm
from models import User
from storage import JsonStorage


class TestOrm(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tmp_path = Path(self.temp_dir.name)
        self.json_storage = JsonStorage(str(self.tmp_path / "test.json"))
        self.orm_ = orm.ORM(self.json_storage)
        self.addCleanup(self.temp_dir.cleanup)

    def test_init_invalid_storage(self):
        with self.assertRaises(ValueError):
            orm.ORM("not_a_storage_object")

    def test_create(self):
        user = User("test_user", "test@email.com")
        self.orm_.create(user)
        self.assertIn(user, self.orm_.get_all())

    def test_get_all(self):
        user1 = User("user1", "user1@email.com")
        user2 = User("user2", "user2@email.com")
        self.orm_.create(user1)
        self.orm_.create(user2)

        all_users = self.orm_.get_all()
        self.assertEqual(len(all_users), 2)
        self.assertIn(user1, all_users)
        self.assertIn(user2, all_users)

    def test_get_by_id_found(self):
        user = User("target_user", "target@email.com")
        self.orm_.create(user)

        fetched_user = self.orm_.get_by_id(user.id)
        self.assertIsNotNone(fetched_user)
        self.assertEqual(fetched_user.id, user.id)
        self.assertEqual(fetched_user.username, "target_user")

    def test_get_by_id_not_found(self):
        fetched_user = self.orm_.get_by_id(uuid.uuid4())
        self.assertIsNone(fetched_user)

    def test_update(self):
        user = User("old_name", "old@email.com")
        self.orm_.create(user)

        updated_user = User("new_name", "new@email.com")
        self.orm_.update(user.id, updated_user)

        fetched_user = self.orm_.get_by_id(user.id)
        self.assertEqual(fetched_user.username, "new_name")
        self.assertEqual(fetched_user.email, "new@email.com")
        self.assertEqual(fetched_user.id, user.id)

    def test_delete(self):
        user = User("to_delete", "delete@email.com")
        self.orm_.create(user)
        self.assertEqual(self.orm_.count(), 1)

        self.orm_.delete(user.id)
        self.assertEqual(self.orm_.count(), 0)
        self.assertIsNone(self.orm_.get_by_id(user.id))

    def test_filter_by(self):
        user1 = User("alice", "alice@email.com")
        user2 = User("bob", "bob@email.com")
        user3 = User("alice", "alice2@email.com")

        self.orm_.create(user1)
        self.orm_.create(user2)
        self.orm_.create(user3)

        filtered = self.orm_.filter_by("username", "alice")
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]["username"], "alice")
        self.assertEqual(filtered[1]["username"], "alice")

    def test_sort_by(self):
        user1 = User("zebra", "zebra@email.com")
        user2 = User("apple", "apple@email.com")
        user3 = User("mango", "mango@email.com")

        self.orm_.create(user1)
        self.orm_.create(user2)
        self.orm_.create(user3)

        sorted_users = self.orm_.sort_by("username")
        self.assertEqual(len(sorted_users), 3)
        self.assertEqual(sorted_users[0].username, "apple")
        self.assertEqual(sorted_users[1].username, "mango")
        self.assertEqual(sorted_users[2].username, "zebra")

    def test_count(self):
        self.assertEqual(self.orm_.count(), 0)
        self.orm_.create(User("user1", "u1@email.com"))
        self.assertEqual(self.orm_.count(), 1)
        self.orm_.create(User("user2", "u2@email.com"))
        self.assertEqual(self.orm_.count(), 2)

    def test_count_where(self):
        self.orm_.create(User("group_a", "1@email.com"))
        self.orm_.create(User("group_a", "2@email.com"))
        self.orm_.create(User("group_b", "3@email.com"))

        self.assertEqual(self.orm_.count_where("username", "group_a"), 2)
        self.assertEqual(self.orm_.count_where("username", "group_b"), 1)
        self.assertEqual(self.orm_.count_where("username", "group_c"), 0)


if __name__ == "__main__":
    unittest.main()
