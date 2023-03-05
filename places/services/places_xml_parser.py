from typing import Optional

from bs4 import BeautifulSoup

from places.constants import PlaceRole
from places.models import Place, PlaceTextAppearance
from texts.models import Text


class PlacesXMLParser:
    ROLE_MAP = {
        PlaceRole.SEND_FROM: 'sent',
        PlaceRole.RECEIVED_IN: 'received',
    }

    def __init__(self, file_soup: BeautifulSoup) -> None:
        self.soup = file_soup
        self.send_from = self.get_send_from()
        self.received_in = self.get_received_in()
        self.mentions = self.get_mentions()

    def create_text_appearances(self, text: Text) -> None:
        if self.send_from:
            PlaceTextAppearance.objects.create(
                text=text,
                place=self.send_from,
                role=PlaceRole.SEND_FROM,
            )
        if self.received_in:
            PlaceTextAppearance.objects.create(
                text=text,
                place=self.received_in,
                role=PlaceRole.RECEIVED_IN,
            )
        for mention in self.mentions:
            PlaceTextAppearance.objects.create(
                text=text,
                place=mention,
                role=PlaceRole.MENTION,
            )

    def get_send_from(self) -> Optional[Place]:
        return self._get_place(PlaceRole.SEND_FROM)

    def get_received_in(self) -> Optional[Place]:
        return self._get_place(PlaceRole.RECEIVED_IN)

    def get_mentions(self):
        all_places = self.soup.select('text placeName')
        return [
            self._parse_place(place_data)
            for place_data in all_places
        ]

    def _parse_place(self, place_data):
        key = place_data.attrs.get('key')
        place, _ = Place.objects.get_or_create(
            key=key,
            defaults={
                'geonames_reference': place_data.attrs.get('ref', None),
            }
        )
        if place_data.get_text() and place_data.get_text() != key:
            place.altered_names.add(place_data.get_text())
        return place

    def _get_place(self, role) -> Optional[Place]:
        place_data = self.soup.select_one(
            f'correspAction[type="{self.ROLE_MAP.get(role)}"] settlement'
        )
        if place_data:
            return self._parse_place(place_data)
