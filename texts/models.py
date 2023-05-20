from django.core.validators import FileExtensionValidator
from django.db import models

from persons.constants import PersonRole
from places.constants import PlaceRole
from texts.constants import Languages


class Text(models.Model):
    file = models.FileField(
        'plik',
        validators=[FileExtensionValidator(['xml'])],
        upload_to='texts',
    )
    title = models.CharField('tytuł', max_length=200)
    publication_statement = models.CharField(max_length=1000)
    source_description = models.CharField('opis źródła', max_length=1000)
    language = models.CharField('język', choices=Languages.choices, max_length=3)
    send_date = models.DateField('data wysłania', null=True, blank=True)
    content = models.TextField('treść', default='')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia')

    class Meta:
        verbose_name = 'Teskty'
        verbose_name_plural = 'Teksty'

    def __str__(self) -> str:
        return f'{self.title} ({self.file.name})'

    @property
    def author(self):
        author_appearance = self.appearing_persons.filter(role=PersonRole.AUTHOR).first()
        if author_appearance:
            return author_appearance.person

    @property
    def receiver(self):
        receiver_appearance = self.appearing_persons.filter(role=PersonRole.RECEIVER).first()
        if receiver_appearance:
            return receiver_appearance.person

    @property
    def send_from(self):
        return self.appearing_places.filter(role=PlaceRole.SEND_FROM).first()

    @property
    def receive_in(self):
        return self.appearing_places.filter(role=PlaceRole.RECEIVED_IN).first()
