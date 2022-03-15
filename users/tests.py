import json
import random
import string

from django.test import TestCase
from django.urls import reverse

from .models import User


# Create your tests here.


def gen_random_normal_str(length: int) -> str:
    result = ""
    for _ in range(length):
        result += random.sample(string.ascii_lowercase + string.digits, 1)[0]
    return result


correct_username = gen_random_normal_str(15)
correct_password = gen_random_normal_str(128)

long_username = gen_random_normal_str(21)
short_username = ""

long_password = gen_random_normal_str(129)
short_password = gen_random_normal_str(127)


class UserModelTest(TestCase):

    # def test_create_user_with_user_already_exist_question(self):
    #     pass

    def test_is_valid_with_error_format_question(self):
        """
        `is_valid()` returns False for User with wrong format

        1. username not in range 1 to 20
        2. password length not equal to 128, which should be encrypted by sha3-512 on client side
        3. salt length not equal to 128, for safety
        """

        # Correct
        self.assertEqual(User.is_valid(username=correct_username, unencrypted_password=correct_password), True)

        # Username
        self.assertEqual(User.is_valid(username=short_username, unencrypted_password=correct_username), False)
        self.assertEqual(User.is_valid(username=long_username, unencrypted_password=correct_username), False)

        # Password
        self.assertEqual(User.is_valid(username=correct_username, unencrypted_password=short_password), False)
        self.assertEqual(User.is_valid(username=correct_username, unencrypted_password=long_password), False)


class UserViewTest(TestCase):
    url_create = reverse("user:create")
    url_login = reverse("user:login")
    url_logout = reverse("user:logout")
    url_destroy = reverse("user:destroy")

    my_username = "pcrab"
    my_password = "35c68888cbf6fee9c1819187c13fe959aa2a456ddcfc44c7684a980719671b8762239397a33f2e3e77ad3ec0848f67a45fa7ef81681d4f8184a0281d52bc624e"

    def create(self, username: str, password: str) -> int:
        return self.client.post(self.url_create,
                                json.dumps({"username": username,
                                            "password": password}),
                                "application/json").status_code

    def login(self, username: str, password: str) -> int:
        return self.client.post(self.url_login,
                                json.dumps({"username": username,
                                            "password": password}),
                                "application/json").status_code

    def logout(self, username: str, password: str) -> int:
        return self.client.post(self.url_logout).status_code

    def destroy(self, username: str, password: str) -> int:
        return self.client.post(self.url_destroy,
                                json.dumps({"username": username,
                                            "password": password}),
                                "application/json").status_code

    def setUp(self) -> None:
        """
        Create test user for following tests.
        """
        print("setup!")
        self.assertEqual(self.create(self.my_username,
                                     self.my_password), 200)

    def test_create_user_wrong_format_question(self):
        """
        respond code equals BadRequest if format is wrong
        """
        self.assertEqual(self.create(correct_username, short_password), 400)

    def test_login_user_error_question(self):
        """
        visit `/user/login/` respond code equals BadRequest(400) if wrong format, or NotFound(404) if user not exist
        """

        # Syntax
        self.assertEqual(self.login(self.my_username, long_password), 400)

        # Wrong Password
        self.assertEqual(self.login(self.my_username, correct_password), 404)

        # Correct
        self.assertEqual(self.login(self.my_username,
                                    self.my_password),
                         404)

    def test_logout_user_error_question(self):
        pass
