from bs4 import BeautifulSoup

from persons.constants import PersonRole
from persons.models import Person, PersonTextAppearance


class PersonXmlParser:
    ROLE_MAP = {
        PersonRole.AUTHOR: 'sent',
        PersonRole.RECEIVER: 'received',
    }

    def __init__(self, file_soup: BeautifulSoup) -> None:
        self.soup = file_soup
        self.author = self.get_author()
        self.receiver = self.get_receiver()
        self.mentions = self.get_mentions()

    def create_text_appearances(self, text):
        PersonTextAppearance.objects.create(
            text=text,
            person=self.author,
            role=PersonRole.AUTHOR,
        )
        PersonTextAppearance.objects.create(
            text=text,
            person=self.receiver,
            role=PersonRole.RECEIVER,
        )
        for mentioned_person in self.mentions:
            PersonTextAppearance.objects.create(
                text=text,
                person=mentioned_person,
                role=PersonRole.MENTION,
            )

    def get_author(self) -> Person:
        return self._get_person(PersonRole.AUTHOR)

    def get_receiver(self) -> Person:
        return self._get_person(PersonRole.RECEIVER)

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

    def _get_person(self, role: PersonRole) -> Person:
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
