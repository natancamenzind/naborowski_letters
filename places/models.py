from django.db import models
from taggit.managers import TaggableManager

from places.constants import PlaceRole


class Place(models.Model):
    key = models.CharField('klucz', max_length=128, unique=True, db_index=True)
    altered_names = TaggableManager('występuje jako')
    geonames_reference = models.URLField('odnośnik do geonames', blank=True, null=True)
    appearance = models.ManyToManyField('texts.Text', through='PlaceTextAppearance')

    class Meta:
        verbose_name = 'Miejsce'
        verbose_name_plural = 'Miejsca'

    def __str__(self) -> str:
        return self.key


class PlaceTextAppearance(models.Model):
    text = models.ForeignKey(
        'texts.Text',
        on_delete=models.CASCADE,
        verbose_name='tekst',
        related_name='appearing_places',
    )
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        verbose_name='osoba',
        related_name='text_appearances',
    )
    role = models.PositiveSmallIntegerField(choices=PlaceRole.choices)

    class Meta:
        verbose_name = 'Miejsce wystepujące w tekście'
        verbose_name_plural = 'Miejsca występujace w tekście'

    def __str__(self) -> str:
        return f'{self.place.key} w "{self.text.title}" ({self.get_role_display()})'

