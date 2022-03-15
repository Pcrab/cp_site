from secrets import compare_digest

import argon2.exceptions
from argon2 import PasswordHasher
from django.db import models


# Create your models here.

_username_len = 20
_password_len = 128

class User(models.Model):
    username = models.CharField(max_length=_username_len, unique=True)
    password = models.CharField(max_length=_password_len)

    def __str__(self):
        return f"username: {self.username}" + '\n' + f"password: {str(self.password)}"

    @staticmethod
    def create_user(username: str, unencrypted_password: str) -> bool:
        try:
            password = _encrypt(unencrypted_password)
            if User.is_exist_unsafe(username=username):
                return False
            user = User(username=username, password=password)
            user.save()
            return True
        except ValueError:
            return False

    @staticmethod
    def is_exist_unsafe(username: str) -> bool:
        user = User._get_user_unsafe(username=username)
        if user:
            return True
        return False

    @staticmethod
    def is_exist(username: str, unencrypted_password: str) -> bool:
        user = User._get_user_unsafe(username=username)
        if user:
            return _check_password(unencrypted_password, user.password)
        return False

    @staticmethod
    def _get_user_unsafe(username: str):
        try:
            user = User.objects.get(username=username)
            return user
        except models.ObjectDoesNotExist:
            return None

    @staticmethod
    def destroy(username: str, unencrypted_password: str) -> bool:
        user = User._get_user_unsafe(username)
        if _check_password(unencrypted_password, user.password):
            user.delete()
            return True
        return False

    @staticmethod
    def is_valid(username: str, unencrypted_password: str) -> bool:
        if 0 < len(username) <= _username_len and len(unencrypted_password) == _password_len:
            return True
        return False

    def check_password(self, password: str) -> bool:
        return _check_password(self.password, password)


def _encrypt(password: str) -> str | None:
    ph = PasswordHasher()
    return ph.hash(password)


def _check_password(password: str, hashed_password: str) -> bool:
    ph = PasswordHasher()

    try:
        ph.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False
