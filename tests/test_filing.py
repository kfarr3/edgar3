from edgar3 import filing


def test_filing():
    with open("tests/raw_filing.txt", "r") as fin:
        fil = filing.Filing(fin.read())
    assert isinstance(fil, filing.Filing)
