from django.db import models

from places.constants import PlaceRole


class Place(models.Model):
    key = models.CharField('klucz', max_length=128, unique=True, db_index=True)
    geonames_reference = models.URLField('odnośnik do geonames', blank=True, null=True)
    appearance = models.ManyToManyField('texts.Text', through='PlaceTextAppearance')

    class Meta:
        verbose_name = 'Miejsce'
        verbose_name_plural = 'Miejsca'

    def __str__(self) -> str:
        return self.key

    @property
    def altered_names(self):
        return ', '.join(set(self.text_appearances.values_list('appears_as', flat=True)))


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
        verbose_name='miejsce',
        related_name='text_appearances',
    )
    role = models.PositiveSmallIntegerField(
        verbose_name='rola',
        choices=PlaceRole.choices,
    )
    appears_as = models.CharField(
        'występuje jako',
        default='',
        max_length=100,
    )
    context = models.CharField(
        'kontekst wystąpienia',
        default='',
        max_length=500,
    )

    class Meta:
        verbose_name = 'Miejsce wystepujące w tekście'
        verbose_name_plural = 'Miejsca występujace w tekście'

    def __str__(self) -> str:
        return f'{self.place.key} w "{self.text.title}" ({self.get_role_display()})'
