import datetime
import pandas as pd
import numpy as np
from edgar3 import edgar_index
from typing import Dict
import httpx

CIK_INDEX = "https://www.sec.gov/Archives/edgar/cik-lookup-data.txt"


def get_13f_listings(date: datetime.datetime, populate: bool) -> pd.DataFrame:
    ed_i = edgar_index.edgar_index()
    df = ed_i.get_full_listing_as_pd(date)
    df = df[df["Form Type"].isin(["13F-HR", "13F-HR/A", "13F-NT", "13F-NT/A"])].reset_index(drop=True)
    df["File"] = np.nan
    if populate:
        for index, row in df.iterrows():
            df["File"] = ed_i.get_filing(row["File Name"])
    return df


def get_raw_cik_numbers() -> str:
    return httpx.get(CIK_INDEX).text


def process_cik_numbers(raw_cik_text: str) -> Dict[str, str]:
    ret = {}
    for line in raw_cik_text.split("\n"):
        if len(line) == 0:
            continue
        parts = line.split(":")
        if len(parts) < 2:
            continue
        ret[parts[1]] = parts[0]
    return ret
