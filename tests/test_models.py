import unittest

import models


class TestModels(unittest.TestCase):
    def test_to_dict(self):
        user = models.User("test_user", "test@email.com")

        dict_user = user.to_dict()

        expected_dict = {
            "id": str(user._id),
            "created_at": user._created_at.strftime("%d-%m-%Y, %H:%M:%S"),
            "username": "test_user",
            "email": "test@email.com",
        }

        self.assertEqual(dict_user, expected_dict)
