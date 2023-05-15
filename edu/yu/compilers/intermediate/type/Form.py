from enum import Enum


class Form(Enum):
    SCALAR = 1
    ENUMERATION = 2
    SUBRANGE = 3
    ARRAY = 4
    RECORD = 5
    UNKNOWN = 6

    def __str__(self):
        return self.name.lower()
