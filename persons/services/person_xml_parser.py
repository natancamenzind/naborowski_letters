from typing import Dict

from persons.constants import Role
from persons.models import Person


class PersonXmlParser:
    ROLE_MAP = {
        Role.AUTHOR: 'sent',
        Role.RECEIVER: 'received',
    }

    def __init__(self, file_soup) -> None:
        self.soup = file_soup

    def get_all_persons_dict(self) -> Dict:
        return {
            Role.AUTHOR: self.get_author(),
            Role.RECEIVER: self.get_receiver(),
        }

    def get_author(self) -> Person:
        return self.get_person(Role.AUTHOR)

    def get_receiver(self) -> Person:
        return self.get_person(Role.RECEIVER)

    def get_person(self, role: Role) -> Person:
        person_data = self.soup.select_one(
            f'correspAction[type="{self.ROLE_MAP.get(role)}"] persName'
        )
        person, _ = Person.objects.get_or_create(
            key=person_data.attrs.get('key'),
            defaults={
                'first_name': person_data.forename.get_text(),
                'last_name': person_data.surname.get_text(),
            }
        )
        return person
