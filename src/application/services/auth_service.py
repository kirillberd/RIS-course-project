from dataclasses import dataclass
from infrastructure.repositories.user_repository import UserRepository
from domain.user import BaseUser
import logging

module_logger = logging.getLogger()

@dataclass
class AuthService:
    user_repository: UserRepository



    def register_user(self, user: BaseUser):
        self.user_repository.add(user)