from enum import Enum


class Status(Enum):
    SET = "set"
    INVALID = "invalid"
    FIRST_LIFE = "first_life"
    SECOND_LIFE = "second_life"
    PURE_SEQUENCE = "pure_sequence"
    IMPURE_SEQUENCE = "impure_sequence"
    FIRST_LIFE_REQUIRED = "first_life_required"
    SECOND_LIFE_REQUIRED = "second_life_requred"
