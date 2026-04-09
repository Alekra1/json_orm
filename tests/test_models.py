import unittest

import models


class TestModels(unittest.TestCase):
    def test_to_dict(self):
        user = models.User("test_user", "test@email.com")

        dict_user = user.to_dict()

        expected_dict = {
            "id": str(user.id),
            "created_at": user.created_at.strftime("%d-%m-%Y, %H:%M:%S"),
            "username": "test_user",
            "email": "test@email.com",
        }

        self.assertEqual(dict_user, expected_dict)

    def test_from_dict(self):
        data = {
            "id": "12345678-1234-5678-1234-567812345678",
            "created_at": "25-12-2025, 10:30:00",
            "username": "test_user",
            "email": "test@email.com",
        }
        user_from_dict = models.User.from_dict(data)
        self.assertEqual(user_from_dict.to_dict(), data)

    def test_eq_same_user(self):
        user = models.User()
        self.assertEqual(user, user)

    def test_eq_different_users(self):
        user1 = models.User()
        user2 = models.User()
        self.assertNotEqual(user1, user2)

    def test_eq_different_objects_same_id(self):
        user1 = models.User("test_user", "test@email.com")
        data = user1.to_dict()
        user2 = models.User.from_dict(data)
        self.assertEqual(user1, user2)

    def test_eq_different_types(self):
        user = models.User()
        self.assertNotEqual(user, "I am not a user, I am just a string")

    def test_username_invalid(self):
        with self.assertRaises(ValueError):
            models.User(username="a")

    def test_username_valid(self):
        user = models.User(username="valid_name")
        self.assertEqual(user.username, "valid_name")

    def test_email_invalid(self):
        with self.assertRaises(ValueError):
            models.User(email="not a valid email")

    def test_email_valid(self):
        user = models.User(email="good@email.com")
        self.assertEqual(user.email, "good@email.com")

    def test_permissions(self):
        user = models.User()
        admin_user = models.AdminUser()
        self.assertEqual(user.get_permissions(), ["read", "write"])
        self.assertEqual(
            admin_user.get_permissions(), ["read", "write", "delete", "manage_users"]
        )

    def test_repr(self):
        user = models.User("test", "test@email.com")
        admin = models.AdminUser("admin", "admin@email.com")

        self.assertTrue(repr(user).startswith("User("))
        self.assertTrue(repr(admin).startswith("AdminUser("))
