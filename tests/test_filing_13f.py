from edgar3 import edgar as ed
from edgar3.filing_13f import Filing_13F
from typing import Dict


def test_filing_13f_holdings_1():
    with open("tests/raw_filing_1.txt", "r") as fin:
        fil = Filing_13F(fin.read())
    fil.process()
    assert isinstance(fil, Filing_13F)
    assert len(fil.header) == 1090
    assert len(fil.documents["13F-HR"]) == 2792
    assert len(fil.documents["INFORMATION TABLE"]) == 56148
    assert len(fil.holdings) == 111
    assert fil.accession_number == "0000919574-18-001804"
    assert fil.holdings[25].name_of_issuer == "DXC TECHNOLOGY CO"
    assert fil.holdings[25].title_of_class == "COM"
    assert fil.holdings[25].cusip == "23355L106"
    assert fil.holdings[25].value == 5731000
    assert fil.holdings[25].number == 60389
    assert fil.holdings[25].type == "SH"


def test_filing_13f_holdings_2():
    with open("tests/raw_filing_2.txt", "r") as fin:
        fil = Filing_13F(fin.read())
    fil.process()
    assert isinstance(fil, Filing_13F)
    assert len(fil.header) == 784
    assert len(fil.documents["13F-HR"]) == 17279
    assert len(fil.holdings) == 117
    assert fil.accession_number == "0000002230-00-000003"
    assert fil.holdings[14].name_of_issuer == "BAXTER INTERNATIONAL"
    assert fil.holdings[14].title_of_class == "COM"
    assert fil.holdings[14].cusip == "071813109"
    assert fil.holdings[14].value == 16017000
    assert fil.holdings[14].number == 255000
    assert fil.holdings[14].type == "SH"
    assert fil.holdings[116].name_of_issuer == "WILMINGTON TRUST CORP."
    assert fil.holdings[116].title_of_class == "COM"
    assert fil.holdings[116].cusip == "971807102"
    assert fil.holdings[116].value == 10133000
    assert fil.holdings[116].number == 210000
    assert fil.holdings[116].type == "SH"


def test_filing_13f_holdings_4():
    with open("tests/raw_filing_4.txt", "r") as fin:
        fil = Filing_13F(fin.read())
    fil.process()
    assert isinstance(fil, Filing_13F)
    assert len(fil.header) == 1057
    assert len(fil.documents["13F-HR"]) == 357905
    assert len(fil.holdings) == 2972
    assert fil.accession_number == "0000003133-00-000001"
    assert fil.holdings[60].name_of_issuer == "AEGON N V"
    assert fil.holdings[60].title_of_class == "COM"
    assert fil.holdings[60].cusip == "007924103"
    assert fil.holdings[60].value == 197000
    assert fil.holdings[60].number == 2064
    assert fil.holdings[60].type == "SH"
    assert fil.holdings[2971].name_of_issuer == "ZILA INC."
    assert fil.holdings[2971].title_of_class == "COM"
    assert fil.holdings[2971].cusip == "989513205"
    assert fil.holdings[2971].value == 3000
    assert fil.holdings[2971].number == 1000
    assert fil.holdings[2971].type == "SH"


def test_filing_13f_client_1():
    with open("tests/raw_filing_1.txt", "r") as fin:
        fil = Filing_13F(fin.read())
    fil.process()
    assert isinstance(fil, Filing_13F)
    assert len(fil.header) == 1090
    assert len(fil.documents["13F-HR"]) == 2792
    assert len(fil.documents["INFORMATION TABLE"]) == 56148
    assert fil.accession_number == "0000919574-18-001804"
    assert fil.manager_name == "KINGDON CAPITAL MANAGEMENT, L.L.C."
    assert fil.street1 == "152 West 57th Street"
    assert fil.street2 == "50th Floor"
    assert fil.city == "New York"
    assert fil.state_or_country == "NY"
    assert fil.zip_code == "10019"
    assert fil.cik == "0001000097"
    assert fil.period_of_report == "12-31-2017"
    assert fil.signature_date == "02-14-2018"


def test_filing_13f_client_2():
    with open("tests/raw_filing_2.txt", "r") as fin:
        fil = Filing_13F(fin.read())
    fil.process()
    assert isinstance(fil, Filing_13F)
    assert len(fil.header) == 784
    assert len(fil.documents["13F-HR"]) == 17279
    assert fil.accession_number == "0000002230-00-000003"
    assert fil.manager_name == "ADAMS EXPRESS CO"
    assert fil.street1 == "SEVEN ST PAUL ST STE 1140"
    assert fil.street2 == ""
    assert fil.city == "BALTIMORE"
    assert fil.state_or_country == "MD"
    assert fil.zip_code == "21202"
    assert fil.cik == "0000002230"
    assert fil.period_of_report == "12-31-1999"
    assert fil.signature_date == "02-15-2000"


def test_filing_13f_client_3():
    with open("tests/raw_filing_3.txt", "r") as fin:
        fil = Filing_13F(fin.read())
    fil.process()
    assert isinstance(fil, Filing_13F)
    assert len(fil.header) == 1004
    assert len(fil.documents["13F-HR"]) == 2378
    assert len(fil.documents["INFORMATION TABLE"]) == 214601
    assert fil.accession_number == "0000007789-19-000010"
    assert fil.manager_name == "ASSOCIATED BANC-CORP"
    assert fil.street1 == "433 MAIN STREET"
    assert fil.street2 == ""
    assert fil.city == "GREEN BAY"
    assert fil.state_or_country == "WI"
    assert fil.zip_code == "54301"
    assert fil.cik == "0000007789"
    assert fil.period_of_report == "12-31-2018"
    assert fil.signature_date == "02-13-2019"
