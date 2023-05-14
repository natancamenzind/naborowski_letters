from dataclasses import dataclass

from persons.models import Person


@dataclass
class PersonAppearance:
    person: Person
    context: str
    appears_as: str
