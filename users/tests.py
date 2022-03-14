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
correct_salt = gen_random_normal_str(128)

long_password = gen_random_normal_str(129)
short_password = gen_random_normal_str(127)

long_salt = gen_random_normal_str(129)
short_salt = gen_random_normal_str(127)


class UserModelTest(TestCase):

    def test_create_user_with_user_already_exist_question(self):
        pass

    def test_is_valid_with_error_format_question(self):
        """
        `is_valid()` returns False for User with wrong format

        1. username not in range 1 to 20
        2. password length not equal to 128, which should be encrypted by sha3-512 on client side
        3. salt length not equal to 128, for safety
        """
        username_too_short = User(username="", password=correct_password, salt=correct_salt)
        self.assertIs(username_too_short.is_valid(), False)
        username_too_long = User(username=gen_random_normal_str(21), password=correct_password, salt=correct_salt)
        self.assertIs(username_too_long.is_valid(), False)

        password_too_short = User(username=correct_username, password=short_password, salt=correct_salt)
        self.assertIs(password_too_short.is_valid(), False)
        password_too_long = User(username=correct_username, password=long_password, salt=correct_salt)
        self.assertIs(password_too_long.is_valid(), False)

        salt_too_short = User(username=correct_username, password=correct_password, salt=short_salt)
        self.assertIs(salt_too_short.is_valid(), False)
        salt_too_long = User(username=correct_username, password=correct_password, salt=long_salt)
        self.assertIs(salt_too_long.is_valid(), False)

        valid_user = User(username=correct_username, password=correct_password, salt=correct_salt)
        self.assertIs(valid_user.is_valid(), True)


class UserViewTest(TestCase):
    def test_create_user_wrong_format_question(self):
        """
        respond code equals BadRequest if format is wrong
        """
        url = reverse("user:create")
        response = self.client.post("/user/create/",
                                    json.dumps({"username": correct_username, "password": short_password}),
                                    "application/json")
        self.assertEqual(response.status_code, 400)

    def test_login_user_error_question(self):
        """
        visit `/user/login/` respond code equals BadRequest(400) if wrong format, or NotFound(404) if user not exist
        """
        url = reverse("user:login")
        response = self.client.post(url,
                                    json.dumps({"username": correct_username, "password": correct_password}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 404)
        response = self.client.post("/user/login/",
                                    json.dumps({"username": "pcrab", "password": "asdf"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 400)
