"""
Splitting the collection of school data into three separate scripts:
getURNs.py      Creates a list of current URNs => School names
download.py     Downloads data for those URNs
extract.py      Extracts all data into a single table

"""

# import time
import pandas as pd
import datetime
import glob

urns = glob.glob('data\\csv\\*.csv')
# urns = urns[:10]  # select 10 from list to test

first = True
for urn in urns:
    print('Processing', urn)
    df = pd.read_csv(urn)
    df.drop(columns=['No'], inplace=True)
    if first:
        first = False
        full_df = df[['Namespace', 'Variable', 'Description']]

    # get school name
    schname = df.loc[(df.Variable =='SCHNAME')].Value.unique()[0]
    df.rename(columns={'Value': schname}, inplace=True)
    full_df = pd.merge(full_df, df, on=['Namespace', 'Variable', 'Description'], how='outer')


# Sort namespace so the useful stuff comes first.
full_df.Namespace = full_df.Namespace.astype('category')
cats = ['L', 'CENSUS_25', 'KS4_25', 'KS4_PUPDEST_25', 'ABS_24', 'KS5_25', 'KS5_STUDEST_25','KS2_25']
full_df.Namespace = full_df.Namespace.cat.set_categories(cats)
full_df.sort_values('Namespace', inplace=True)

filedate = datetime.date.today().strftime('%Y%m%d')
outpath = 'data/' + filedate + '_GIAS.csv'
full_df.to_csv(outpath, index=False)

