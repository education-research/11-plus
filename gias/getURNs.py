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
import zipfile
import os
import glob

"""
It would be possible to fully automate the download but probably more effort than benefit.
Manual steps:   
Download the latest "all establishment data" from here:
https:/get-information-schools.service.gov.uk/Downloads
This should end up here:
'C:/Users/User/Downloads/

%userprofile%/downloads/extract.zip

The filename will be something like edubasealldata20260120.csv. 

Filter this on 
EstablishmentStatus (name) = "Open"
PhaseOfEducation (name) = "Secondary"

"""

# The DfE may change what they call things and the following assignments may need modifying.
zippy = 'extract.zip'
csv = 'edubasealldata*csv'
cols = ['URN', 'EstablishmentName', 'EstablishmentStatus (name)', 'PhaseOfEducation (name)', 'AdmissionsPolicy (name)']

# Define the path to the zip file
zip_file_path = os.path.join(os.environ['USERPROFILE'], 'Downloads', zippy)

# Extract the zip file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(os.path.join(os.environ['USERPROFILE'], 'Downloads'))

# Read the CSV file into a DataFrame
csv_file_path = glob.glob(os.path.join(os.environ['USERPROFILE'], 'Downloads', csv))[0]
df = pd.read_csv(csv_file_path, usecols=cols, encoding = 'ISO-8859-1')

# Remove spacese from column headers!
df.columns = ['URN', 'SchoolName', 'Status', 'Phase', 'AdmPolicy']

"""
Filter this on 
EstablishmentStatus (name) = "Open"
PhaseOfEducation (name) = "Secondary"

"""

df = df.loc[(df.Status == 'Open')]
df = df.loc[(df.Phase == 'Secondary')]

df.to_csv('data/URNs.csv', index=False)
