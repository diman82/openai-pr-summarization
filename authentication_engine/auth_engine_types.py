from enum import Enum, unique
from abc import ABC, abstractmethod


@unique
class AuthEngine(Enum):
    BASIC = "basic"
    OAUTH = "oauth"


class BaseAuth(ABC):
    @abstractmethod
    def authenticate(self) -> bool:
        # TODO: add some shared logic here
        pass
