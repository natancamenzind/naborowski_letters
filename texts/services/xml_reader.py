from typing import Dict

from bs4 import BeautifulSoup

from texts.constants import title_field_map, Languages


class XMLReader:
    def __init__(self, file_content) -> None:
        self.soup = BeautifulSoup(file_content, 'xml')

    def get_text_dict(self) -> Dict:
        return {
            model_field: self.clean_field(xml_filed_name)
            for xml_filed_name, model_field in title_field_map.items()
        } | {'language': self.get_language()}

    def clean_field(self, field_name: str) -> str:
        val = self.soup.find(field_name).text
        return val.replace('\n', '')

    def get_language(self) -> str:
        return self.soup.find('language').get('ident') or Languages.POLISH.value
