# %%
from edgar3 import edgar
import datetime

ed = edgar.edgar()

date_index = datetime.datetime(2018, 1, 2)

# %%
print("index: " + ed.get_full_listing_as_pd(date_index))


# %%
