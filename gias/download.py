"""
Splitting the collection of school data into three separate scripts:
getURNs.py      Creates a list of current URNs => School names
download.py     Downloads data for those URNs
extract.py      Extracts all data into a single table

"""

import time
import pandas as pd
from urllib.request import Request, urlopen  # Python 3
import datetime
from random import randint
from time import sleep

# Read the URN list created by getURNs.py
df = pd.read_csv('data/URNs.csv')

# make a note of the *download* date (more important than URNs list update?)
filedate = datetime.date.today().strftime('%Y%m%d')

# Define where to write the output ...
csvdir = 'data/csv'
# Unlikely, but if certain browsers were excluded later this would need updating.
ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'
# This is more likely to change.
api = 'https://www.compare-school-performance.service.gov.uk/download-school-data?urn='

def dl_url(u):
    """
    :param u: URN of the school. Must be a string not an integer.
    :return: Dataframe containing everything relating to the school with that URN
    """
    url = api + u
    print('calling ' + url)
    req = Request(url)
    req.add_header('User-Agent', ua)
    return pd.read_csv(urlopen(req), encoding='utf-8')

# kend = dl_url('136448')  # test this function with specific fixed URN.

ss = df.__len__()
si = 1
failed = []
for u in df.URN:
    # print('downloading ' + str(u))
    try:
        sch = dl_url(str(u))
        sch.to_csv(csvdir + '/' + str(u) + '.csv', index=False)
        si += 1
    except:
        failed.append(str(u))
    paws = randint(2, 10)
    pct = (si * 100) / ss
    #print("{:.2f}".format(your_float))
    print(str(si) + ' out of ' + str(ss) + ' ({:.2f}%) downloaded. Pausing for '.format(pct) + str(paws) + ' seconds.')
    sleep(paws)


# The Try/Except doesn't seem to work! The main loop that iterates of URNs modified to print out progress
# If (when!) it gets stuck, the best solution is probably to kill the script, manually edit the csv file to remove
# the ones already downloaded and restart.
