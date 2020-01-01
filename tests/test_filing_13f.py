from edgar3.filing_13f import Filing_13F


def test_filing_13f():
    with open("tests/raw_filing.txt", "r") as fin:
        fil = Filing_13F(fin.read())
    fil.process_information_table()
    assert isinstance(fil, Filing_13F)
    assert len(fil.header) == 1090
    assert len(fil.documents["13F-HR"]) == 2792
    assert len(fil.documents["INFORMATION TABLE"]) == 56148
    assert len(fil.holdings) == 111
    assert fil.holdings[25].nameOfIssuer == "DXC TECHNOLOGY CO"
    assert fil.holdings[25].titleOfClass == "COM"
    assert fil.holdings[25].cusip == "23355L106"
    assert fil.holdings[25].value == 5731000
    assert fil.holdings[25].number == 60389
    assert fil.holdings[25].type == "SH"
