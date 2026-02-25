
"""
Times Parent Power is the most authoritative source for information about which schools are best. Although this is 
self-declared judging by literally 100s of national and local press linking to them, it is true. All the more
scary as they STILL report which schools are best based on raw test (a problem I highlighted a decade ago).  

The problem with data published on the web is it can more around but at the time of writing these URLs are valid:

Top state secondary schools:
https://dlv.tnl-parent-power.gcpp.io/2024?filterId=the-top-state-secondary-schools 
This tag contains all the data in json format
<tbody class="pp-main-table-2023__table--content-group pp-main-table-2024__table--content-group">


... and whilst I have Chrome inspector open, other query strings that might be of interest
Top comprehensive and partial comps:
https://dlv.tnl-parent-power.gcpp.io/2024?filterId=the-top-state-secondary-comprehensive-schools 

Top state comps: (list only goes down to 159 to save the blushes of the last four!)  
https://dlv.tnl-parent-power.gcpp.io/2024?filterId=the-top-state-secondary-selective-schools

Top 50 sixth forms (Kings Maths School conducts interviews which is not allowed in the Code.) 
https://dlv.tnl-parent-power.gcpp.io/2024?filterId=the-top-75-sixth-form-colleges


"""

# documentation, including some examples, is here https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup
import numpy as np

url = 'https://dlv.tnl-parent-power.gcpp.io/2024?filterId=the-top-state-secondary-schools'
html = request.urlopen(url).read()
soup2 = BeautifulSoup(html, 'html.parser')
# soup2 contains the whole page. This returns the specific table with headers
table = soup2.find_all('table', class_='pp-main-table-2023__table')
# print(table)
# table = soup2.find_all('table')  # also seems to work without specifying the class
# https://stackoverflow.com/questions/50633050/scrape-tables-into-dataframe-with-beautifulsoup#56510975
df = pd.read_html(str(table))[0]

# Table headers end up in the last row so lose that row.
df = df.head(df.__len__() - 2)

# Add the headings used by PP (with gaps removed!)
df.columns = ['Rank', 'School', 'Town', 'Type', 'A-level(%A*)', 'A-level(% A*/A)', 'A-level(%A*/B)',
              'A-level_rank', 'GCSE_(%9/8/7)', 'GCSE_rank', 'blank1', 'blank2']

# Col 10 is a gender icon which is blank. Col 11 is also blank. Remove both.
df = df.drop(df.columns[[10, 11]], axis=1)

# Every other row is blank (nan) so remove.
df = df.dropna()
# df = df.reset_index()
# Parent Power uses a fancy single quote. To link to DfE will probably be semi-manual so may as well remove.
df['School'] = df.School.str.replace("’", "'")
df['Town'] = df.Town.str.replace("’", "'")

# GCSE rank shows equal ranks with '=' breaking what would otherwise be a nice integer field :-/
df['GCSE_rank'] = df.GCSE_rank.str.replace("=", "")
df.GCSE_rank = pd.to_numeric(df.GCSE_rank, errors='coerce').fillna(0).astype(np.int64)
df = df.sort_values('GCSE_rank')  # :-)

# (A-level) Rank has two values - the rank and the change since last year! :-/
df['Rank'] = df.Rank.str.replace(" .*", "")
df['Rank'] = df.Rank.str.replace("=", "")
df.Rank = pd.to_numeric(df.Rank, errors='coerce').fillna(0).astype(np.int64)

# Type column is string either: Selective (100%), Partially selective (xx%), or Comprehensive.
# I *could* write code to fix this, but it takes five mins in Excel so ...
df.to_csv('C:/_python/test_reliability/data/ParentPower.csv')
