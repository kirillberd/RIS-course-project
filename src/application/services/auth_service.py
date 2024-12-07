from dataclasses import dataclass
from infrastructure.providers.sql_provider import SQLProvider
from infrastructure.repositories.user_repository import UserRepository
from domain.user import BaseUser, UserLogin
from pymysql import IntegrityError
from infrastructure.exceptions.auth_errors import (
    UserAlreadyExistsError,
    IncorrectPasswordError,
    IncorrectUsernameError,
)
import logging
import bcrypt

module_logger = logging.getLogger()


@dataclass
class AuthService:
    user_repository: UserRepository
    sql_provider: SQLProvider

    def register_user(self, user: BaseUser):
        try:
            password_hashed = self._hash_user_password(user.password)
            user.password = password_hashed
            query = self.sql_provider.get("create_user.sql", **user.model_dump())
            self.user_repository.add(query)
        except IntegrityError:
            raise UserAlreadyExistsError("Пользователь с данным именем уже существует.")

    def login(self, user_login: UserLogin) -> BaseUser:
        try:
            query = self.sql_provider.get("get_user.sql", username=user_login.username)
            user = self.user_repository.get_one(query)
        except Exception as e:
            module_logger.error(e)
            raise IncorrectUsernameError(
                    "Пользователя с даннным именем не существует. Пройдите регистрацию или попробуйте другое имя."
                )
        if self._validate_user_password(user_login.password, user.password):
            return user
        else:
            raise IncorrectPasswordError("Неверный пароль.")
       
    def login_as_admin(self, user_login: UserLogin) -> BaseUser:
        try:
            query = self.sql_provider.get("get_internal_user.sql", username=user_login.username)
            user = self.user_repository.get_one(query)
        except Exception as e:
            module_logger.error(e)
            raise IncorrectUsernameError(
                    "Пользователя с даннным именем не существует. Пройдите регистрацию или попробуйте другое имя."
                )
        if user_login.password == user.password:
            return user
        else:
            raise IncorrectPasswordError("Неверный пароль.")   

    def _hash_user_password(self, password: str):
        salt = bcrypt.gensalt()
        password_hashed = bcrypt.hashpw(password.encode("utf-8"), salt).decode()
        return password_hashed

    def _validate_user_password(self, password: str, password_hashed: str):
        password_bytes = password.encode()
        password_hashed_bytes = password_hashed.encode()
        return bcrypt.checkpw(password_bytes, password_hashed_bytes)
