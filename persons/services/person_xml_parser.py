from bs4 import BeautifulSoup, Tag

from persons.constants import PersonRole
from persons.data_classes import PersonAppearance
from persons.models import Person, PersonTextAppearance
from texts.utils import extract_context_sentence


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

    def create_text_appearances(self, text: str) -> None:
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
                role=PersonRole.MENTION,
                person=mentioned_person.person,
                context=mentioned_person.context,
                appears_as=mentioned_person.appears_as,
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
        return person

    def _get_person(self, role: PersonRole) -> Person:
        person_data = self.soup.select_one(
            f'correspAction[type="{self.ROLE_MAP.get(role)}"] persName'
        )
        return self.parse_person(person_data)

    def _create_person_appearance(self, person_data: Tag) -> PersonAppearance:
        return PersonAppearance(
            person=self.parse_person(person_data),
            context=extract_context_sentence(
                self.soup,
                'persName',
                person_data.attrs.get('key'),
            ),
            appears_as=person_data.get_text()
        )

    def get_mentions(self) -> list[PersonAppearance]:
        all_persons = self.soup.select('persName')
        return [
            self._create_person_appearance(person_data)
            for person_data in all_persons
            if person_data.attrs.get('key') not in [self.author.key, self.receiver.key]
        ]
