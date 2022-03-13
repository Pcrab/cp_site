import hashlib
import random
import string

from django.db import models


# Create your models here.

# class UserErrorEnum(IntFlag):
#     UsernameNotFound = auto()
#     PasswordNotCorrect = auto()
#     FormatNotCorrect = auto()

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    salt = models.CharField(max_length=128)

    def __str__(self):
        return self.username + '\n' + self.password + '\n' + self.salt

    @staticmethod
    def create_user(user) -> None:
        salt = create_salt(len(user["password"]))
        password = encrypt(user["password"], salt)
        user = User(username=user["username"], password=password, salt=salt)
        if user.is_valid():
            user.save()
            return
        raise UserCreateException("Invalid User")

    @staticmethod
    def is_exist_unsafe(username: str) -> bool:
        if User.objects.filter(username=username):
            return True
        return False

    @staticmethod
    def is_exist(username: str, password: str) -> bool:
        if User.objects.filter(username=username, password=password):
            return True
        return False

    def is_valid(self) -> bool:
        if 0 < len(self.username) <= 20 and 128 == len(self.password) == len(self.salt):
            return True
        return False


class UserException(Exception):
    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorInfo = ErrorInfo

    def __str__(self):
        return self.errorInfo


class UserCreateException(UserException):
    pass


def create_salt(length) -> str:
    result = ""
    for _ in range(length):
        result += random.sample(string.ascii_lowercase + string.digits, 1)[0]
    return result


def encrypt(password: str, salt: str) -> str | None:
    if len(password) != len(salt):
        return None
    for _ in range(100):
        sh = hashlib.sha3_512()
        password += salt
        sh.update(password.encode("utf-8"))
        password = sh.hexdigest()

    return password
