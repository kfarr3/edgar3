# SEC.gov Filing parsing

from typing import Tuple, Dict


class Filing:
    header = ""
    documents = None  # type: Dict[str, str]

    def __init__(self, filing: str):
        self.header, filing2 = self._extract_section(filing, "<SEC-HEADER>", "</SEC-HEADER>")

        if self.documents is None:
            self.documents = {}

        document, filing = self._extract_section(filing2, "<DOCUMENT>", "</DOCUMENT>")
        while len(document) > 0:
            tag = self._extract_tag(document, "<TYPE>")
            self.documents[tag] = document
            document, filing = self._extract_section(filing, "<DOCUMENT>", "</DOCUMENT>")

    def __repr__(self):
        ret = "Filings with\n"
        ret += " Header of Length: {0}\n".format(len(self.header))
        for key in self.documents:
            ret += " Document ({0}) of Length: {1}\n".format(key, len(self.documents[key]))
        return ret

    def _extract_section(self, filing: str, section_start: str, section_end: str) -> Tuple[str, str]:
        start = filing.find(section_start)
        end = filing.find(section_end)
        if start == -1 or end == -1:
            return "", filing  # not found
        section = filing[start + len(section_start) + 1 : end]
        filing = filing[end + len(section_end) + 1 :]
        return section, filing

    def _extract_tag(self, document: str, tag: str) -> str:
        start = document.find(tag)
        end = document.find("\n", start)
        if start == -1 or end == -1:
            return ""  # not found
        return document[start + len(tag) : end]
