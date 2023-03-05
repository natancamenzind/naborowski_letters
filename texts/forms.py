from django import forms
from django.core.validators import FileExtensionValidator

from persons.services.person_xml_parser import PersonXmlParser
from places.services.places_xml_parser import PlacesXMLParser
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
        instance = super().save(commit=False)
        instance.save()
        PersonXmlParser(reader.soup).create_text_appearances(instance)
        PlacesXMLParser(reader.soup).create_text_appearances(instance)
        return instance
