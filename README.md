# High Stakes Academic Selection in England. 
The data and code underpinning research into the "11-plus" school admissions tests used by schools in England. 
*Keywords*: Socio-Economic Circumstances; Social Justice/equity; Education Policy; Political Economic and Cultural Contexts; Secondary education; Assessment; Quantitative Methods; Exploratory studies
## The data.
Data relating to the English 11-plus test is generally exceedingly difficult to obtain for independent research but there are some gems here! These include
- Test results linked to candidates Free School Meal entitlement (a useful if somewhat crude indicator of children from lower socio-economic groups)
- Results linked to IDACI (Income Deprivation Affecting Children Index, a continual measure of SES.) 
- Results linked to candidates' age. (Relatively older children, born at the beginning of the school year, perform slightly better than their year group colleagues born towards the end of the year.)
- The "league tables" published by a newspaper. 
- Copies of official data openly published by the Department for Education (but not always easy to find.) 
## The code.
The code is 100% Python. Github incorrectly reports 98% HTML because there is ONE dynamic HTML file. This displays a dynamic Sankey diagram in a web browser but it's ONE (huge) file!

The code will run under any text based Python installation eg Pycharm, IPython, Visual Studio etc. or even at the command line. 

Most code would probably run if cut and paste into Jupyter Console. I think the graphing environment in the web gui would need some customisation.

Initially all scripts read any input data from the ./data on local drive. Scripts are all being modified to directly load data from this github repository. 

Scripts also output results to the local ./data directory. With hindsight, calling this ./output would have been more sensible! Scripts are also being modified to do that. If ./output doesn't exist, scripts *will* crash!

The traditional format for papers is typically something like:
- Introduction
- Methodology
  - Data collection
  - Data analysis
- Results
- Discussion. 
The code documents the methodology. Running it creates the results. Each script has comments saying what it does and why but if something is not clear please get in touch via [Discussions](https://github.com/education-research/11-plus/discussions/1.)
Output results are either:
- Data written as csv files. These will be modified to include the name of the script which generated them, or
- Graphs in png format. These already include the name of the script and line number so a graph can be traced back to the code and data used to create it.
There are also lines of code commented out which write interim results to csv. Uncommenting them can help understand how the data is being processed. 
## The structure of this repository
Nov 2026 - reorganising this repository around four main directories: code, data, docs, output. (gias and spc contain copies of public domain data published by the DfE.) Contents of each should be self explanatory. I will add a README to the code and data directories. I also need to modify all the code to match this structure (reading data direct from github, writing to ./output, ensuring csv output data referencing the code which created them.) 
