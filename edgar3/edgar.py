# SEC.GOV Edgar Interface

import requests
import pandas as pd
import datetime
import json

# https://www.sec.gov/edgar/searchedgar/accessing-edgar-data.htm

daily_index = 'https://www.sec.gov/Archives/edgar/daily-index'
full_index = 'https://www.sec.gov/Archives/edgar/full-index'
archives_url = 'https://www.sec.gov/Archives'
edgar_url = 'https://www.sec.gov/Archives/edgar'

_known_daily_index = {}
_known_full_index = {}

def _get_quarter(month: int):
    # Quarters are  
    # QTR1 1-3
    # QTR2 4-6
    # QTR3 7-9
    # QTR4 10-12
    
    if (month <= 3): return 1
    elif (month <= 6): return 2
    elif (month <= 9): return 3
    else: return 4

def _get_full_index_url(date: datetime):
    quarter = _get_quarter(date.month)
    return "{full_index}/{year}/QTR{quarter}/index.json".format(full_index=full_index, year=date.year, quarter=quarter)

def _get_daily_index_url(date: datetime):
    quarter = _get_quarter(date.month)
    return "{daily_index}/{year}/QTR{quarter}/index.json".format(daily_index=daily_index, year=date.year, quarter=quarter)

def _get_full_index(date: datetime):
    quarter = _get_quarter(date.month)
    key = "{year}_{quarter}".format(year=date.year, quarter=quarter)

    if key in _known_full_index:
        return _known_full_index[key]
    else:
        index = json.loads(requests.get(_get_full_index_url(date)).text)
        _known_full_index[key] = index
        return index

def _get_daily_index(date: datetime):
    quarter = _get_quarter(date.month)
    key = "{year}_{quarter}".format(year=date.year, quarter=quarter)

    if key in _known_daily_index:
        return _known_daily_index[key]
    else:
        index = json.loads(requests.get(_get_daily_index_url(date)).text)
        _known_daily_index[key] = index
        return index

def _get_full_listing_url(date: datetime):
    # master.idx
    file_name = "master.idx"

    index_dic = _get_full_index(date)

    for item in index_dic['directory']['item']:
        if item['name'] == file_name:
            return ("{edgar_url}/{parent}{file_name}".format(edgar_url=edgar_url,parent=index_dic['directory']['name'], file_name=file_name),True)

    return ("",False)

def _get_daily_listing_url(date: datetime):
    # master.20180102.idx
    file_name = "master.{year}{month:02d}{day:02d}.idx".format(year=date.year, month=date.month, day=date.day)

    index_dic = _get_daily_index(date)

    for item in index_dic['directory']['item']:
        if item['name'] == file_name:
            return ("{edgar_url}/{parent}{file_name}".format(edgar_url=edgar_url,parent=index_dic['directory']['name'], file_name=file_name),True)

    return ("",False)

def get_full_listing(date: datetime):
    listing_url,status = _get_full_listing_url(date)
    if status is False:
        return ""
    return requests.get(listing_url).text

def get_daily_listing(date: datetime):
    listing_url,status = _get_daily_listing_url(date)
    if status is False:
        return ""
    return requests.get(listing_url).text

def get_full_listing_as_pd(date: datetime):
    listing = get_full_listing(date)
    return _format_listing_as_pd(listing, date)

def get_daily_listing_as_pd(date: datetime):
    listing = get_daily_listing(date)
    return _format_listing_as_pd(listing, date)

def _format_listing_as_pd(listing: str, date: datetime):
    if len(listing)==0: return None

    raw_rows = listing.splitlines()

    # validate header to be removed
    if not raw_rows[0].startswith("Description:"): raise Exception("Failed header check: Description")
    if not raw_rows[1].startswith("Last Data Received:"): raise Exception("Failed header check: Last Data Received")
    if not raw_rows[2].startswith("Comments:"): raise Exception("Failed header check: Comments")
    if not raw_rows[3].startswith("Anonymous FTP:"): raise Exception("Failed header check: Anonymous FTP")

    if raw_rows[4].startswith("Cloud HTTP:"):
        skip=5
        while len(raw_rows[skip]) <=1:
            skip += 1
        if not raw_rows[skip].startswith('CIK|Company Name|Form Type|Date Filed|Filename'): raise Exception("Failed header check: Cloud, Column Names")
        if not raw_rows[skip+1].startswith('--------------------------------------------------------------------------------'): raise Exception("Failed header check: Cloud, Data Seperator")
        skip += 2
    else:

        if not len(raw_rows[4]) <=1: raise Exception("Failed header check: Line 5 not empty")
        if not raw_rows[5] == 'CIK|Company Name|Form Type|Date Filed|File Name': raise Exception("Failed header check: Column names")
        if not raw_rows[6] == '--------------------------------------------------------------------------------': raise Exception("Failed header check: Data Seperator")
        skip=7

    df = pd.read_csv(pd.compat.StringIO(listing), sep='|', index_col=False, skiprows=skip, names=['CIK','Company Name','Form Type','Date Filed','File Name'])
    df['Date Found'] = int("{year}{month:02d}{day:02d}".format(year=date.year, month=date.month, day=date.day))
    return df

def get_filing_list(ciks: [int], start_date: datetime, end_date: datetime):
    df = None
    for day in range((end_date - start_date).days + 1):
        date = start_date+datetime.timedelta(days=day)
        if date.isoweekday() <= 5:
            df_test = get_daily_listing_as_pd(date)
            if df_test is None: 
                continue

            df_test = df_test.loc[df_test['CIK'].isin(ciks)]
            if df is None:
                df = df_test
            else:
                df = pd.concat([df,df_test], ignore_index=True)
    return df
            
def get_filing(url: str):
    return requests.get("{archives_url}/{url}".format(archives_url=archives_url, url=url)).text

