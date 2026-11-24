# High Stakes Academic Selection in England. 
The data and code underpinning independent research into the "11-plus" school admissions tests used by schools in England. This is currently under blind peer review so there is no information here linking to the author but anonymous contact is possible via [Discussions](https://github.com/education-research/11-plus/discussions/1.). 

*Keywords*: Socio-Economic Circumstances; Social Justice/equity; Education Policy; Political Economic and Cultural Contexts; Secondary education; Assessment; Quantitative Methods; Exploratory studies
## The data.
Data relating to the English 11-plus test is incredibly difficult to source for independent research but there are some gems here which include
- Test results linked to candidates Free School Meal entitlement (a useful if somewhat crude indicator of children from lower socio-economic groups)
- Results linked to IDACI (Income Deprivation Affecting Children Index, a continuous rather than discrete measure of SES.) 
- Results linked to candidates' age. (Relatively older children, born at the beginning of the school year, perform slightly better than their year group colleagues born towards the end of the year.)

Also copies of relevant official data published by the Department for Education but not always easy to find.
## The code.
The code is **100% Python**. Github incorrectly reports 98% HTML due to ONE gargantuan DHTML file created by plotly which displays a dynamic Sankey diagram in a web browser! It seems GitHub determines what a repository contains based on total bytes rather than number of files.

The code will run under any text based Python installation eg Pycharm, IPython, Visual Studio etc. or even at the command line. 

Most code would probably run if cut and paste into Jupyter Console but the graphing environment would need some customisation. Jupyter looks pretty, but I'm not a fan.

Initially all scripts read any input data they needed from the ./data on local drive. Code is all being modified to directly load data from this GitHub repository. I may miss some! Look for pd.read_csv() in the code.

Scripts also output results to the local **./data** directory. With hindsight, calling this **./output** would have been a lot more sensible! Code is also being modified to change this path. If ./output (or possibly ./data) doesn't exist, scripts **will** 100% guaranteed crash!

The traditional format for papers goes something like this:
- Introduction
- Methodology
  - Data collection
  - Data analysis
- Results
- Discussion. 

Each script has comments at the top saying what it does and why documenting the *Methodology*. Running it creates the *Results*. Between them this covers the 'evidence' sections of any paper, but if anything is not clear please get in touch via [Discussions](https://github.com/education-research/11-plus/discussions/1.)
Output results are either:
- Data written as csv files. These will be modified to include the name of the script which generated them, or
- Graphs in png format. These already include the name of the script and line number so a graph can be traced back to the code and data used to create it.
There are also lines of code commented out which write interim results to csv. Uncommenting them can help understand how the data is being processed. 
## The structure of this repository
Nov 2026 - reorganising this repository around four main directories: code, data, docs, output. (gias and spc contain copies of public domain data published by the DfE.) Contents of each should be self explanatory. I will add a README to the code and data directories. I also need to modify all the code to match this structure (reading data direct from github, writing to ./output, ensuring csv output data referencing the code which created them.) 
