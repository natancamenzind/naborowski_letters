from django.db import models

title_field_map = {
    'title': 'title',
    'publicationStmt': 'publication_statement',
    'sourceDesc': 'source_description',
}


class Languages(models.TextChoices):
    LATIN = 'lat', 'łacina'
    POLISH = 'pl', 'polski'
