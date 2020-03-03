# edgar3

Edgar3 was originally created to scrape 13f files from SEC's Edgar database and convert them into Pandas DataFrames

It works great to download all filings, and then to process them into Python objects, or into Pandas Dataframes.

Get a raw listing with

```python
listings_df = ed.get_13f_listings(datetime.datetime(2020, 1, 1), True)
```

Once you have a listing, you can turn it into a Filing with

```python
fil = Filing_13F(listing_df['File Name'][0])
fil.process()
```

This library has been used to download all 35 Terabytes of 13F Filings from 2000-2020, turn them all (2014+) into Python objects, and load into a database for later processing.