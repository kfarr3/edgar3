from edgar3 import __version__, edgar
import datetime


def test_version():
    assert __version__ == "edgar3 version 1.0"


def test_get_quarter():
    ed = edgar.edgar()
    assert ed._get_quarter(1) == 1
    assert ed._get_quarter(2) == 1
    assert ed._get_quarter(3) == 1
    assert ed._get_quarter(4) == 2
    assert ed._get_quarter(5) == 2
    assert ed._get_quarter(6) == 2
    assert ed._get_quarter(7) == 3
    assert ed._get_quarter(8) == 3
    assert ed._get_quarter(9) == 3
    assert ed._get_quarter(10) == 4
    assert ed._get_quarter(11) == 4
    assert ed._get_quarter(12) == 4
    assert ed._get_quarter(0) == 1
    assert ed._get_quarter(13) == 4


def test_get_full_index_url():
    ed = edgar.edgar()
    assert ed._get_full_index_url(datetime.date(2018, 1, 1)) == "https://www.sec.gov/Archives/edgar/full-index/2018/QTR1/index.json"
    assert ed._get_full_index_url(datetime.date(2018, 8, 1)) == "https://www.sec.gov/Archives/edgar/full-index/2018/QTR3/index.json"
    assert ed._get_full_index_url(datetime.date(2019, 2, 1)) == "https://www.sec.gov/Archives/edgar/full-index/2019/QTR1/index.json"
    assert ed._get_full_index_url(datetime.date(2019, 4, 1)) == "https://www.sec.gov/Archives/edgar/full-index/2019/QTR2/index.json"
    assert ed._get_full_index_url(datetime.date(2019, 7, 1)) == "https://www.sec.gov/Archives/edgar/full-index/2019/QTR3/index.json"
    assert ed._get_full_index_url(datetime.date(2019, 12, 1)) == "https://www.sec.gov/Archives/edgar/full-index/2019/QTR4/index.json"


def test_get_daily_index_url():
    ed = edgar.edgar()
    assert ed._get_daily_index_url(datetime.date(2018, 1, 1)) == "https://www.sec.gov/Archives/edgar/daily-index/2018/QTR1/index.json"
    assert ed._get_daily_index_url(datetime.date(2018, 8, 1)) == "https://www.sec.gov/Archives/edgar/daily-index/2018/QTR3/index.json"
    assert ed._get_daily_index_url(datetime.date(2019, 2, 1)) == "https://www.sec.gov/Archives/edgar/daily-index/2019/QTR1/index.json"
    assert ed._get_daily_index_url(datetime.date(2019, 4, 1)) == "https://www.sec.gov/Archives/edgar/daily-index/2019/QTR2/index.json"
    assert ed._get_daily_index_url(datetime.date(2019, 7, 1)) == "https://www.sec.gov/Archives/edgar/daily-index/2019/QTR3/index.json"
    assert ed._get_daily_index_url(datetime.date(2019, 12, 1)) == "https://www.sec.gov/Archives/edgar/daily-index/2019/QTR4/index.json"


def test_get_full_index():
    ed = edgar.edgar()
    index_dict = ed._get_full_index(datetime.date(2018, 1, 1))

    assert len(index_dict) == 1
    assert list(index_dict.keys()) == ["directory"]
    assert list(index_dict["directory"].keys()) == ["item", "name", "parent-dir"]
    assert len(index_dict["directory"]["item"]) == 28
    assert index_dict["directory"]["name"] == "full-index/2018/QTR1/"
    assert list(index_dict["directory"]["item"][0].keys()) == ["last-modified", "name", "type", "href", "size"]
