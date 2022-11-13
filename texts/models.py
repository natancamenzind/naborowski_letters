from django.core.validators import FileExtensionValidator
from django.db import models

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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='data utworzenia')

    class Meta:
        verbose_name = 'Teskty'
        verbose_name_plural = 'Teksty'

    def __str__(self) -> str:
        return f'{self.title} ({self.file.name})'
