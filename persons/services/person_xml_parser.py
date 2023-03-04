from typing import Dict

from bs4 import BeautifulSoup

from persons.constants import Role
from persons.models import Person, TextAppearance


class PersonXmlParser:
    ROLE_MAP = {
        Role.AUTHOR: 'sent',
        Role.RECEIVER: 'received',
    }

    def __init__(self, file_soup: BeautifulSoup) -> None:
        self.soup = file_soup
        self.author = self.get_author()
        self.receiver = self.get_receiver()
        self.mentions = self.get_mentions()

    def create_text_appearances(self, text):
        all_persons_dict = self.get_all_persons_dict()
        TextAppearance.objects.create(
            text=text,
            person=all_persons_dict.get(Role.AUTHOR),
            role=Role.AUTHOR,
        )
        TextAppearance.objects.create(
            text=text,
            person=all_persons_dict.get(Role.RECEIVER),
            role=Role.RECEIVER,
        )
        for mentioned_person in self.mentions:
            TextAppearance.objects.create(
                text=text,
                person=mentioned_person,
                role=Role.MENTION,
            )

    def get_all_persons_dict(self) -> Dict:
        return {
            Role.AUTHOR: self.author,
            Role.RECEIVER: self.receiver,
            Role.MENTION: self.mentions,
        }

    def get_author(self) -> Person:
        return self.get_person(Role.AUTHOR)

    def get_receiver(self) -> Person:
        return self.get_person(Role.RECEIVER)

    def parse_person(self, person_data) -> Person:
        person, _ = Person.objects.get_or_create(
            key=person_data.attrs.get('key'),
            defaults={
                'first_name':
                    person_data.forename.get_text() if person_data.forename else '',
                'last_name':
                    person_data.surname.get_text() if person_data.surname else '',
            }
        )
        person.altered_names.add(person_data.get_text())
        return person

    def get_person(self, role: Role) -> Person:
        person_data = self.soup.select_one(
            f'correspAction[type="{self.ROLE_MAP.get(role)}"] persName'
        )
        return self.parse_person(person_data)

    def get_mentions(self):
        all_persons = self.soup.select('persName')
        return [
            self.parse_person(person_data)
            for person_data in all_persons
            if person_data.attrs.get('key') not in [self.author.key, self.receiver.key]
        ]
