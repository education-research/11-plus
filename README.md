# The 11-plus exam and its lack of transparency, objectivity, and fairness. 
This repository contains the data and code underpinning research into the "11-plus" school admissions tests used by schools in England which has been submitted to a journal for peer review. 
## Abstract
The 11-plus exam is a high-stakes test taken by 10-year-olds in England used to determine admission to academically selective grammar schools. This paper argues it fails to meet three core principles, transparency, objectivity, and fairness, which underpin the Schools Admissions Code, the statutory framework under which school admissions must operate. The research applies measurement theory to objectively determine how well selective admission arrangements, predicated on this exam, meet each of these statutory obligations and how the system could be improved.
The exam is the only high stakes test not regulated by the Office of Qualifications and Examinations Regulation (Ofqual) and the way it operates is exceptionally opaque. There is no information about its reliability, how scores are adjusted to cater for different age candidates, or how the results are rescaled so the number of children ‘passing’ enables grammar schools to always fill places. These issues stem from the conflict of interests the government created by introducing "market forces" to the education system then allowing schools to determine their own admissions arrangements. 
Our research finds that the test perpetuates social segregation as it is biased against less affluent children, noting the effect this has on test scores is seven or eight times greater than the effect of candidates’ relative age within the cohort. The latter is always compensated for through "age-weighting", but no adjustments are made to the scores of children from under-resourced backgrounds. 
The paper concludes that the 11-plus is not fit for purpose. We defer to existing literature on whether academic selection delivers overall benefits. If it must persist, a more transparent, objective, and fair method of selection is needed. This needs to be regulated by Ofqual, and it must account for socioeconomic factors. 
## Keywords
Socio-Economic Circumstances; Social Justice/equity; Education Policy; Political Economic and Cultural Contexts; Secondary education; Assessment; Quantitative Methods; Exploratory studies
## Structure of the paper.
The statutory guidance for admissions to state funded schools in England is based on three key criteria: transparency, objectivity, and fairness. Academically selective admissions are predicated on the admissions test (commonly called "the 11-plus".) The paper investigates how these key criteria are met. Underpinning that are several appendixes which cover the quantitative research briefly 
## 11-plus survey
Over 90% of secondary schools now determine their own admission arrangements. The proportion for selective "grammar" schools is 95%. The test is not regulated by Ofqual or monitored by the Department for Education. The research captures the size and cost of the 2024 test. [The results](https://github.com/education-research/11-plus/blob/main/data/2024-11-plus-survey-results.xlsx) are shared in this repository. 
## Reliability and Validity
Information on the reliability and validity of this high-stakes test is not disclosed by the grammar schools and/or test providers. This section calculates occasion reliability and confidence intervals and the classification accuracy of the test, both for a single candidate and for selecting a cohort predicted to do well in their final exams. 
## School Measures
Since the 1980s both Conservative and Labour governments policy has been based on the belief that the delivery of public services is always improved by adding competition. School funding is per capita. Parent "consumers" express their preferences for a given school, informed by "league tables" based on raw exam results. This research compared the "top 400 state schools" published by the leading newspaper against DfE prior attainment figures and found a 95% correlation. At the same time, schools are allowed to select which students they admit, which even the ardent neo-liberal would have to agree is rather dumb.
## Measurement Bias
This section calculates the effect size for three different sources of bias on test scores: i) Coaching, ii) Relative age, iii) Free School Meals eligibility (commonly used as an indicator of children from under-resourced backgrounds. Nothing can be done about coaching beyond acknowledging that the statutory requirement that the test *must* give an accurate reflection of the child’s ability or aptitude is not achievable. It is possible to adjust for the other two measures. We note that age-in-cohort has been adjusted for over a hundred years. Socio-economic status has seven or eight time the effect but this is not adjusted. 
# The data and code. 
The file structure is very simple. Python scripts are in the top-level directory. Below that is a 'data' directory where both input and processed output data as well as any figures used in the paper are held. Output files are named after the script and line they were created so, for example, [yorks-stats-table.py-line72.csv](https://github.com/education-research/11-plus/blob/main/data/yorks-stats-table.py-line72.csv) is a table output by the yorks-stats-table.py at line 72. (Line numbers may drift.) This makes it easier to find the origin of an output file. 
The following sections provide a short description of the code.
### bucks-pp-effect.py
This takes two data sources, the scores of all candidates sitting the test in Buckinghamshire in 2017 and 2018 and the scores of just those entitled to free school meals. These are combined into a single dataset and the [normalised distributions](https://github.com/education-research/11-plus/blob/main/data/bucks-pp-effect.py-line184.png) for each 'treatment' plotted so they can be visually compared.
### class_acc.py
This repeats and corrects an illustration by Coe et al (2008) of the classification accuracy for a test with 0.7 validity concluding about [20.8% are misclassified](https://github.com/education-research/11-plus/blob/main/data/class_acc.py_line142.png). 
### download-times-top.py
This script downloads the 2024 "top 400 state schools" as published by the newspaper.
### ParentPowerPlot-v2.py
This takes the data downloaded by the above, calculates correlations, and plots it against official DfE data.
### effect_size_plots.py
This plots [the effect sizes](https://github.com/education-research/11-plus/blob/main/data/effect_size_plots.py_line62.png) for a control group and the effect of: i) Coaching, ii) Age-in-cohort, iii) Free School Meals eligibility. 
### feldt.py
Feldt et al (1985) calculated Standard Error of Measurement five different ways to demonstrate that SEM is higher in the middle of a range of scores. The similarity between each was remarkable but they published these results in some rather dull tables. The [output](https://github.com/education-research/11-plus/blob/main/data/feldt.png) of this script brings their results to life.
### lincs-gla-log-odds.py
One commercial test provider claimed to have discover a new "proprietary" way to determine statistical bias. This script dispels that myth by calculating this the normal way, using linear regression, then comparing the claimed proprietary method against the orthodox. The former includes a log-odds transformation, published by Ian Schagan (1990). 
### lincs-kent-regression.py
This applies linear regression to multiple sources of data on the 11-plus test where candidates' ages are known to determine a more robust measure of the effect of age within cohort. The results are remarkably similar to other studies, eg Crawford et al (2007)
### lincs-thomson.py
Historically, age in cohort was adjusted by grouping candidates by birth month, using Ordinary Least Squares to find the best fit, and Legrange’s interpolation to fill in the gaps and create a lookup table. This method scaled very well before computer programs emerged in the 1990s to automate this. This script creates a [neat illustration](https://github.com/education-research/11-plus/blob/main/data/thomson-violin.py_line106.png) of how this method works using current data. 
### parliament-figures.py
Parliamentary researches provided the figures for the number of grammar schools and percentage of children they educate since 1965 (Danechi et al). This combines both sources on [a single plot](https://github.com/education-research/11-plus/blob/main/data/parliament-figures.py.png) illustrating how these have diverged over time. 
### sankey_nuts.py
This script got its name because anyone needs to be a bit crazy to attempt to plot the number of candidates sitting the 11-plus broken down by local authority/consortia/individual school and test provider and individual school. The output is a 4MB dynamic HTML file which is too big for GitHub to display. Here is a [static image](https://github.com/education-research/11-plus/blob/main/data/11%2Bsankey-port(2125x3400).png) of the plot. 
### selectiveness-barplot.py
### selectiveness-choropleth.py
Over two thirds of English local authorities have no grammar schools. The proportions, in the others ranges from a couple of percent to over two thirds of all school places. These two scripts take this data and plot it both as a horizontal bar graph and a choropleth map showing location and intensity of selection. 
### SPC.parse.py
### Y6-numbers.py
These two scripts take official data and use it to determine the increase in [schools determining own admissions]( https://github.com/education-research/11-plus/blob/main/data/SPC.parse.py_line_116.png) arrangements since 2010 as well as the number of children in the cohort that sit the 11-plus (in their final year at primary school). 
### yorks-scatter-plots.py
### yorks-stats-table.py
These scripts process the data provided by North Yorks council used to work out the occasion reliability of 11-plus tests repeated one week apart. 


