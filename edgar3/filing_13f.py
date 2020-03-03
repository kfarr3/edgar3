from __future__ import annotations  # this is needed for Holding to return self

from .filing import Filing
import xml.etree.ElementTree as ET
from typing import Dict, List
import datetime
import locale

locale.setlocale(locale.LC_ALL, "en_US.UTF-8")


class Filing_13F(Filing):
    def __init__(self, filing: str):
        super().__init__(filing)
        self.manager_name = ""
        self.cik = ""
        self.period_of_report = ""
        self.signature_date = ""

    def __repr__(self):
        ret = f"13F Filings for {self.manager_name}({self.cik})\n" f" Period: {self.period_of_report}\n" f" Reported: {self.signature_date}\n" f" Header of Length: {0}\n".format(len(self.header))
        for key in self.documents:
            ret += " Document ({0}) of Length: {1}\n".format(key, len(self.documents[key]))
        return ret

    def process(self):
        ret = self._process_13f_hr()
        if ret is not True:
            return ret
        ret = self._process_information_table()
        if ret is not True:
            return ret

        return True

    def _process_information_table(self) -> bool:

        if "INFORMATION TABLE" in self.documents:
            document = self.documents["INFORMATION TABLE"]

            xml_doc, ext = self._extract_section(document, "<XML>", "</XML>")
            if len(xml_doc) == 0:
                return False
            root = ET.fromstring(xml_doc)
            namespace = {"ns1": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}
            self.holdings = []
            for child in root:
                try:
                    holding = Holding().process_xml(child, namespace)
                    self.holdings.append(holding)
                except ValueError as error:
                    print("Error processing Holding:", error)
            return True
        elif "13F-HR" in self.documents:
            # process text version
            self.holdings = []
            started = False
            finished = False
            column_indices: List[int] = []

            for line in self._extract_section(self.documents["13F-HR"], "<TABLE>", "</TABLE>")[0].split("\n"):

                if not started and len(column_indices) == 0:
                    # looking for the starting character of "- --""
                    if line.startswith("- --"):
                        column_indices = [index - 1 for index, c in enumerate(line[1:-1]) if line[index] == " " and line[index + 1] == "-"]
                        column_indices.append(len(line))
                        if len(column_indices) < 5:
                            raise ValueError("Cannot process column_indicies")
                        continue
                else:

                    if len(line.strip()) > 0:
                        parts = [line[column_indices[x] : column_indices[x + 1]].strip().upper() for x in range(len(column_indices) - 1)]
                        try:
                            holding = Holding().process_text(parts)
                            self.holdings.append(holding)
                            started = True
                            if finished:
                                print(f"Was Finished, started again: {line}")
                        except ValueError:
                            if started:
                                # print(f"Error, failed to parse holding after starting: \n'{line}'")
                                finished = True
            return True

        return False

    def _process_header_data(self, root: ET.Element, namespace: Dict[str, str]):
        header_data = _get_element(root, "ns1:headerData", namespace)
        filer_info = _get_element(header_data, "ns1:filerInfo", namespace)
        self.period_of_report = datetime.datetime.strptime(_get_element_text(filer_info, "ns1:periodOfReport", namespace), "%m-%d-%Y").strftime("%Y-%m-%d")

        filer = _get_element(filer_info, "ns1:filer", namespace)
        creds = _get_element(filer, "ns1:credentials", namespace)
        self.cik = _get_element_text(creds, "ns1:cik", namespace)

    def _process_form_data(self, root: ET.Element, namespace: Dict[str, str]):
        form_data = _get_element(root, "ns1:formData", namespace)
        cover_page = _get_element(form_data, "ns1:coverPage", namespace)
        filing_manager = _get_element(cover_page, "ns1:filingManager", namespace)
        self.manager_name = _get_element_text(filing_manager, "ns1:name", namespace)

        address = _get_element(filing_manager, "ns1:address", namespace)
        self.street1 = _get_element_text(address, "ns2:street1", namespace)
        self.street2 = _get_element_text(address, "ns2:street2", namespace, "")
        self.city = _get_element_text(address, "ns2:city", namespace)
        self.state_or_country = _get_element_text(address, "ns2:stateOrCountry", namespace)
        self.zip_code = _get_element_text(address, "ns2:zipCode", namespace)

        signature_block = _get_element(form_data, "ns1:signatureBlock", namespace)
        self.signature_date = datetime.datetime.strptime(_get_element_text(signature_block, "ns1:signatureDate", namespace), "%m-%d-%Y").strftime("%Y-%m-%d")

    def _process_13f_hr(self) -> bool:
        try:
            document = self.documents["13F-HR"]
        except KeyError:
            return False

        # Process as text doc
        # for a text doc, this data is kept in the header
        available_sections = ["FILER:", "COMPANY DATA:", "FILING VALUES:", "BUSINESS ADDRESS:", "MAIL ADDRESS:"]
        section = ""
        for line in self.header.split("\n"):
            line = line.strip().upper()

            if len(line) == 0:
                continue
            # extract out any sections
            if line in available_sections:
                section = line
            else:
                parts = [x.strip().upper() for x in line.split(":")]
                if len(parts) != 2:
                    continue
                if section == "":
                    if parts[0] == "ACCESSION NUMBER":
                        self.accession_number = parts[1]
                    elif parts[0] == "CONFORMED PERIOD OF REPORT":
                        self.period_of_report = datetime.datetime.strptime(parts[1], "%Y%m%d").strftime("%Y-%m-%d")
                    elif parts[0] == "FILED AS OF DATE":
                        self.signature_date = datetime.datetime.strptime(parts[1], "%Y%m%d").strftime("%Y-%m-%d")
                elif section == "COMPANY DATA:":
                    if parts[0] == "COMPANY CONFORMED NAME":
                        self.manager_name = parts[1]
                    elif parts[0] == "CENTRAL INDEX KEY":
                        self.cik = parts[1]
                elif section == "BUSINESS ADDRESS:":
                    if parts[0] == "STREET 1":
                        self.street1 = parts[1]
                        self.street2 = ""
                    elif parts[0] == "STREET 2":
                        self.street2 = parts[1]
                    elif parts[0] == "CITY":
                        self.city = parts[1]
                    elif parts[0] == "STATE":
                        self.state_or_country = parts[1]
                    elif parts[0] == "ZIP":
                        self.zip_code = parts[1]

        xml_doc, ext = self._extract_section(document, "<XML>", "</XML>")
        if len(xml_doc) > 0:
            # process as XML doc
            root = ET.fromstring(xml_doc)
            namespace = {"ns1": "http://www.sec.gov/edgar/thirteenffiler", "ns2": "http://www.sec.gov/edgar/common"}
            self._process_header_data(root, namespace)
            self._process_form_data(root, namespace)

        return True


def _get_element(root: ET.Element, path: str, namespace: Dict[str, str]) -> ET.Element:
    x = root.find(path, namespace)
    if x is None:
        raise ValueError(f"During processing of a 13f, the {path} element was not found on the expected parent")
    return x


def _get_element_text(root: ET.Element, path: str, namespace: Dict[str, str], default: str = None):
    x = root.find(path, namespace)
    if x is None:
        if default is None:
            raise ValueError(f"During processing a 13f, the {path} element was not found on the expected parent, thus no .text")
        else:
            return default
    return x.text


class Holding:
    def __init__(self):
        self.name_of_issuer = ""
        self.cusip = ""

    def process_text(self, parts: List[str]) -> Holding:
        self.name_of_issuer = parts[0]
        self.title_of_class = parts[1]
        self.cusip = parts[2].upper()

        if not self._validate_cusip():
            raise ValueError(f"Invalid cusips {self.cusip}")

        if len(parts[3]) > 0:
            try:
                self.value = locale.atoi(parts[3]) * 1000
            except ValueError:
                print(f"ValueError: value ({self.name_of_issuer})")
                self.value = 0
        else:
            self.value = 0

        if len(parts[4]) > 0:
            try:
                # may be number only
                # may be number and share type UGH
                share_parts = parts[4].split(" ")
                if len(share_parts) > 1:
                    self.number = locale.atoi(share_parts[0])
                    self.type = share_parts[1]
                else:
                    self.number = locale.atoi(parts[4])
            except ValueError:
                print(f"ValueError: number ({self.name_of_issuer})")
                self.number = 0
        else:
            self.number = 0

        # we check if we added above, again UGH
        if not hasattr(self, "type"):
            self.type = parts[5]
        return self

    def process_xml(self, root: ET.Element, namespace: Dict[str, str]) -> Holding:

        self.name_of_issuer = _get_element_text(root, "ns1:nameOfIssuer", namespace, "")
        self.title_of_class = _get_element_text(root, "ns1:titleOfClass", namespace, "")
        self.cusip = _get_element_text(root, "ns1:cusip", namespace, "").upper()

        # if not self._validate_cusip():
        #    raise ValueError(f"Invalid cusips {self.cusip}")
        try:
            self.value = int(float(_get_element_text(root, "ns1:value", namespace, "0"))) * 1000

            shares = root.find("ns1:shrsOrPrnAmt", namespace)

            # not sure if there's a way for additional shares types to be encoded here
            # so we will throw an error if it's not 2
            if shares is None or len(shares) != 2:
                raise ValueError(self.name_of_issuer + ": shrsOrPrnAmt != 2")

            self.number = int(float(_get_element_text(shares, "ns1:sshPrnamt", namespace, "0")))
            self.type = _get_element_text(shares, "ns1:sshPrnamtType", namespace, "")

        except ValueError:
            raise ValueError(self.name_of_issuer)
        except AttributeError:
            raise AttributeError(self.name_of_issuer)
        return self

    def _validate_cusip(self):
        return (len(self.cusip) == 9) and self.cusip.isalnum()

    def __repr__(self):
        ret = self.name_of_issuer + "(${0}:{1} @ {2})".format(self.value, self.number, self.value / self.number)
        return ret
