from typing import Optional

import nltk
from bs4 import BeautifulSoup


def extract_context_sentence(
        soup: BeautifulSoup, tag: str, key: str,
) -> Optional[str]:
    tags = soup.find_all(tag, attrs={'key': key})
    sentences = []
    for t in tags:
        parent = t.parent
        sentences.extend(
            ' '.join(sentence.split())
            for sentence in nltk.sent_tokenize(parent.text)
            if t.text in sentence
        )

    return ' [...] '.join(sentences)
