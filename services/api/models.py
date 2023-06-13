from dataclasses import dataclass
from enum import Enum
from uuid import UUID


class MedicationStatus(str, Enum):
    NULL = "NULL"
    TAKEN = "TAKEN"
    SKIPPED = "SKIPPED"


@dataclass
class Medication:
    id: str
    name: str
    quantity: int
    dose: int

    @classmethod
    def create(cls, id_, name, quantity, dose):
        return cls(id_, name, quantity, dose, MedicationStatus.NULL)


@dataclass
class User:
    id: str
    username: UUID
    email: str
    given_name: str
    family_name: str
