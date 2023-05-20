from datetime import datetime, date
from typing import Optional

from bs4 import BeautifulSoup

from texts.constants import title_field_map, Languages


class XMLReader:
    def __init__(self, file_content) -> None:
        self.soup = BeautifulSoup(file_content, 'xml')

    def get_text_dict(self) -> dict:
        return {
            model_field: self.clean_field(xml_filed_name)
            for xml_filed_name, model_field in title_field_map.items()
        } \
               | {'language': self.get_language()} \
               | {'send_date': self.get_send_date()} \
               | {'content': self.parse_content()}

    def clean_field(self, field_name: str) -> str:
        val = self.soup.find(field_name).text
        return val.replace('\n', '')

    def get_language(self) -> str:
        return self.soup.find('language').get('ident') or Languages.POLISH.value

    def get_send_date(self) -> Optional[date]:
        send_date = self.soup.select_one('correspAction[type="sent"] date').get('when')
        if not send_date:
            return
        return datetime.strptime(send_date, '%Y-%m-%d').date()

    def parse_content(self) -> str:
        return ' '.join(self.soup.stripped_strings)
