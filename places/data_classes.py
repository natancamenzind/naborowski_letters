from dataclasses import dataclass

from places.models import Place


@dataclass
class PlaceAppearance:
    place: Place
    appears_as: str
    context: str
