from dataclasses import dataclass
from infrastructure.providers.sql_provider import SQLProvider
from infrastructure.repositories.user_repository import UserRepository
from domain.user import BaseUser
from pymysql import IntegrityError
from infrastructure.exceptions.auth_errors import UserAlreadyExistsError
import logging
import bcrypt

module_logger = logging.getLogger()

@dataclass
class AuthService:
    user_repository: UserRepository
    sql_provider: SQLProvider

    def register_user(self, user: BaseUser):
        try:
            salt = bcrypt.gensalt()
            password_hashed = self._hash_user_password(user.password)
            user.password = password_hashed
            query = self.sql_provider.get("create_user.sql", **user.model_dump())
            self.user_repository.add(user, query)
        except IntegrityError:
            raise UserAlreadyExistsError("Пользователь с данным username уже существует.")
        

    def _hash_user_password(self, password: str):
        salt = bcrypt.gensalt()
        password_hashed = bcrypt.hashpw(password.encode("utf-8"), salt).decode()
        return password_hashed