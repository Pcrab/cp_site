import random
import string

from django.test import TestCase

from .models import User


# Create your tests here.

def gen_random_normal_str(length: int) -> str:
    result = ""
    for _ in range(length):
        result += random.sample(string.ascii_lowercase + string.digits, 1)[0]
    return result


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
        correct_username = gen_random_normal_str(15)
        correct_password = gen_random_normal_str(128)
        correct_salt = gen_random_normal_str(128)

        username_too_short = User(username="", password=correct_password, salt=correct_salt)
        self.assertIs(username_too_short.is_valid(), False)
        username_too_long = User(username=gen_random_normal_str(21), password=correct_password, salt=correct_salt)
        self.assertIs(username_too_long.is_valid(), False)

        password_too_short = User(username=correct_username, password="123", salt=correct_salt)
        self.assertIs(password_too_short.is_valid(), False)
        password_too_long = User(username=correct_username, password=gen_random_normal_str(129), salt=correct_salt)
        self.assertIs(password_too_long.is_valid(), False)

        salt_too_short = User(username=correct_username, password=correct_password, salt="")
        self.assertIs(salt_too_short.is_valid(), False)
        salt_too_long = User(username=correct_username, password=correct_password, salt=gen_random_normal_str(129))
        self.assertIs(salt_too_long.is_valid(), False)

        valid_user = User(username=correct_username, password=correct_password, salt=correct_salt)
        self.assertIs(valid_user.is_valid(), True)
