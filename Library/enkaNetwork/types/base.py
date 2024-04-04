from enum import Enum

class BaseEnum(Enum):
    @classmethod
    def enumToList(cls):
        return [c.value for c in cls]

class StrEnum(str, BaseEnum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name