from django.db import models
from taggit.managers import TaggableManager

from persons.constants import PersonRole


class Person(models.Model):
    key = models.CharField('klucz', max_length=50, unique=True)
    first_name = models.CharField('imie', max_length=50, default='', blank=True)
    last_name = models.CharField('naziwsko', max_length=50, default='', blank=True)
    altered_names = TaggableManager('inne imiona')
    date_of_birth_start = models.DateField(
        'data narodzin, początek',
        null=True,
        blank=True,
    )
    date_of_birth_end = models.DateField('data narodzin, koniec', null=True, blank=True)
    date_of_death_start = models.DateField(
        'data śmierci, początek',
        null=True,
        blank=True,
    )
    date_of_death_end = models.DateField('data śmierci, koniec', null=True, blank=True)
    life_range_display = models.CharField(
        'zakres dat życia',
        default='',
        blank=True,
        max_length=50,
    )
    description = models.TextField('opis', blank=True, default='')
    appearance = models.ManyToManyField('texts.Text', through='PersonTextAppearance')

    class Meta:
        verbose_name = 'Osoba'
        verbose_name_plural = 'Osoby'

    def __str__(self) -> str:
        return self.key


class PersonTextAppearance(models.Model):
    text = models.ForeignKey(
        'texts.Text',
        on_delete=models.CASCADE,
        verbose_name='tekst',
        related_name='appearing_persons',
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        verbose_name='osoba',
        related_name='text_appearances',
    )
    role = models.PositiveSmallIntegerField(choices=PersonRole.choices)

    class Meta:
        verbose_name = 'Osoba wystepujące w tekście'
        verbose_name_plural = 'Osoby wystepujące w tekście'

    def __str__(self) -> str:
        return f'{self.person.key} w "{self.text.title}" ({self.get_role_display()})'
