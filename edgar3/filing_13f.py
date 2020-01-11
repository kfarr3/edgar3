from .filing import Filing
import xml.etree.ElementTree as ET
from typing import Dict


class Filing_13F(Filing):
    def __init__(self, filing: str):
        super().__init__(filing)

    def __repr__(self):
        ret = "13F Filings with\n"
        ret += " Header of Length: {0}\n".format(len(self.header))
        for key in self.documents:
            ret += " Document ({0}) of Length: {1}\n".format(key, len(self.documents[key]))
        return ret

    def process_information_table(self):
        try:
            document = self.documents["INFORMATION TABLE"]
        except KeyError:
            return False

        xml_doc, ext = self._extract_section(document, "<XML>", "</XML>")
        if len(xml_doc) == 0:
            return False
        root = ET.fromstring(xml_doc)
        namespace = {"ns1": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}
        self.holdings = []
        for child in root:
            try:
                holding = Holding(child, namespace)
                self.holdings.append(holding)
            except ValueError as error:
                print("Error processing Holding:", error)

        return True


class Holding:
    def __init__(self, root: ET.Element, namespace: Dict[str, str]):
        try:
            self.nameOfIssuer = self._get_element_text(root, "ns1:nameOfIssuer", namespace, "")
            self.titleOfClass = self._get_element_text(root, "ns1:titleOfClass", namespace, "")
            self.cusip = self._get_element_text(root, "ns1:cusip", namespace, "")
            self.value = int(self._get_element_text(root, "ns1:value", namespace, "0")) * 1000

            shares = root.find("ns1:shrsOrPrnAmt", namespace)

            # not sure if there's a way for additional shares types to be encoded here
            # so we will throw an error if it's not 2
            if shares is None or len(shares) != 2:
                raise ValueError(self.nameOfIssuer + ": shrsOrPrnAmt != 2")

            self.number = int(self._get_element_text(shares, "ns1:sshPrnamt", namespace, "0"))
            self.type = self._get_element_text(shares, "ns1:sshPrnamtType", namespace, "")

        except ValueError:
            raise ValueError(self.nameOfIssuer)
        except AttributeError:
            raise ValueError(self.nameOfIssuer)

    def _get_element_text(self, root: ET.Element, path: str, namespace: Dict[str, str], default: str):
        x = root.find(path, namespace)
        if x is None:
            return default
        return x.text

    def __repr__(self):
        ret = self.nameOfIssuer + "(${0}:{1} @ {2})".format(self.value, self.number, self.value / self.number)
        return ret


#
# <ns1:informationTable xmlns:ns1="http://www.sec.gov/edgar/document/thirteenf/informationtable">
# 	<ns1:infoTable>
#         <ns1:nameOfIssuer>AMERICAN EXPRESS CO </ns1:nameOfIssuer>
# 		<ns1:titleOfClass>COM</ns1:titleOfClass>
# 		<ns1:cusip>025816109</ns1:cusip>
# 		<ns1:value>27055</ns1:value>
# 		<ns1:shrsOrPrnAmt>
# 			<ns1:sshPrnamt>272430</ns1:sshPrnamt>
# 			<ns1:sshPrnamtType>SH</ns1:sshPrnamtType>
# 		</ns1:shrsOrPrnAmt>
# 		<ns1:investmentDiscretion>SOLE</ns1:investmentDiscretion>
# 		<ns1:votingAuthority>
# 			<ns1:Sole>272430</ns1:Sole>
# 			<ns1:Shared>0</ns1:Shared>
# 			<ns1:None>0</ns1:None>
# 		</ns1:votingAuthority>
# 	</ns1:infoTable>"""
#
