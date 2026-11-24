# High Stakes Academic Selection in England. 
This repository contains the data and code behind underpinning research into the "11-plus" school admissions tests used by schools in England. 
## Keywords
Socio-Economic Circumstances; Social Justice/equity; Education Policy; Political Economic and Cultural Contexts; Secondary education; Assessment; Quantitative Methods; Exploratory studies
## The data.
Data relating to the English 11-plus test is generally exceedingly difficult to obtain for research. This repository includes test results linked to candidates Free School Meal entitlement (a useful if somewhat crude indicator of children from lower socio-economic groups) and IDACI (a direct measure of the same.) It also includes test results linked to candidates' age. Relatively older children, born at the beginning of the school year, perform slightly better than their year group colleagues born towards the end of the year. The repository also includes the "league tables" published by a newspaper as well as relevant official data published by the Department for Education (but not always easy to find.) 
## The code.
The code is 100% Python. Github incorrectly reports 98% HTML because there is ONE dynamic HTML file. This displays a dynamic Sankey diagram in a web browser but it's ONE (huge) file!
The code will run under any Python installation eg Pycharm, IPython etc. or even at the command line. 
Most will probably run if cut and paste into Jupyter Console. I think the graphing requirements in the web gui are different.
Most (all?) scripts expects a ./data directory to exist to write output to. With hindsight, calling this ./output may have been a better choice. (I may make that change.) 
Initially all scripts read data from the ./data on local drive. Am slowly modifying all the code to call data directly from this github repository. 
The traditional format for journal publications might be structured under Methodology (Data collection & data analysis) Results, Discussion. Publishing the code covers the data collection and analysis. Running it creates the results. I endeavour to add comments to each script saying what it does and why but may frequently fall short of perfection. 
## The structure of this repository
Nov 2026 - reorganising this repository around four main directories: code, data, docs, output. (gias and spc contain copies of public domain data published by the DfE.) Contents of each should be self explanatory. I will add a README to the code and data directories. 
