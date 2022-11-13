from django import forms
from django.core.validators import FileExtensionValidator

from texts.models import Text
from texts.services.xml_reader import XMLReader


class XmlFileForm(forms.ModelForm):
    file = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['xml'])]
    )

    class Meta:
        model = Text
        fields = ['file']

    def save(self, commit=True):
        file = self.instance.file.open('r')
        reader = XMLReader(file_content=file.read())
        for key, value in reader.get_text_dict().items():
            setattr(self.instance, key, value)
        return super().save(commit)
