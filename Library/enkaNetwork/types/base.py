from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def enumToList(cls):
        return [c.value for c in cls]