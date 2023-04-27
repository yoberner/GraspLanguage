from enum import Enum


class BackendMode(Enum):
    CONVERTER = 1
    EXECUTOR = 2
    COMPILER = 3
