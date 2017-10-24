# Intro

Policing has become an increasingly divisive issue over the past few years in American public discourse.

The seemingly unending high-profile police shootings of unarmed black men (such as Michael Brown, Tamir Rice, Anton Sterling, and Philando Castile) have catalyzed massive protests against what is seen as a systemic, and often violent, targeting of people-of-color by police forces across the country.

On the other side of the political spectrum, a common belief is that the unbalanced police targeting of non-white citizens is a myth created by the mainstream media based on a handful of extreme cases that are not representative of the national norm.

In June 2017, a team of researchers at Stanford University collected and released an open-source data set of 60 million state police patrol stops from 20 states across the US.  In this tutorial, we walk through how analyze and visualize this data using Python, and we'll work to cut through the political smoke-screens in order to quantitatively determine the existence of systemic racially driven policing bias.

< show chart >

The tutorial and analysis would not be possible without the groundwork put into place by "The Standford Open Policing Project".  Much of the analysis performed in this tutorial is based on the work that has already performed by this team.  A short tutorial for working with the data using the R programming language is provided on the official project website.  The goal of this tutorial is not to present a groundbreaking or original analysis of the dataset; the intention primarily is to provide you with the tools and foundation to dive even deeper into the data on your own.

# The Data

In the United States, there are, on average, more than 50,000 traffic stops every day.  The potential number of data points for each stop is huge, from the demographics (age, race, gender) of the driver, to the location, time of day, stop reason, stop outcome, car model, and much more.  Unfortunately, not every state makes this data available, and those that do often have different reporting standards for what information is recorded.  Even different counties and districts within each state can be inconstant in how each traffic stop is recorded.  The research team at Stanford has managed to gather traffic-stop data from twenty states, and has worked to regularize the reporting standards for 11 fields.

- Stop Date
- Stop Time
- Stop Location
- Driver Race
- Driver Gender
- Driver Age
- Stop Reason
- Search Conducted
- Search Type
- Contraband Found
- Stop Outcome

Most states do not have data available for every field, but there is enough overlap between the data sets to provide a solid foundation for some very interesting analysis.

# 0 - Getting Started

We'll start with analyzing the data set for Vermont.  We're looking at Vermont first for a few reasons.

1. The Vermont dataset is small enough to be very manageable at only 283,285 traffic stops (compared to the Texas data set, for instance, which contains records on almost 24 million stops).
2. There is not much missing data, as all eleven fields mentioned above are covered.
3. Vermont is 94% white, but is also in a part of the country known for being fairly liberal (disclaimer - I grew up in the Boston area, and I've spent a quite a bit of time in Vermont).  Many in this area consider their state very progressive and would like to believe that their state institutions are not terribly prone to systemic racism.  It will be interesting to determine if the data validates this view.

### 0.0 - Download Datset

First download the Vermont traffic stop data - https://stacks.stanford.edu/file/druid:py883nd2578/VT-clean.csv.gz

### 0.1 - Setup Project

Create a new directory for the project, say `police-data-analysis`, and move the downloaded file into a `/data` directory within the project.

### 0.2 - Optional: Create new virtualenv (or Anaconda) environment

If you want to keep your Python dependencies neat and separated between projects, now would be the time to create and activate a new environment for this analysis, using either virtualenv or Anaconda.

I'm not going to go into detail about how to do this, if you want to learn more check out the tutorials here.
virtualenv - LINK
Anaconda - LINK

### 0.3 - Install dependencies

We'll need to install a few Python packages to perform our analysis.

On the command line, run the following to install the required libraries.
```bash
pip install numpy pandas matplotlib jupyter
```

> If you're using Anaconda, you can replace the `pip` command here with `conda`.

### 0.4 - Start Jupyter Notebook

Start a new local Jupyter notebook server from the command line.

```bash
jupyter notebook
```

Open your browser to the specified URL (probably `localhost:8888`, unless you have a special configuration) and create a new notebook.

### 0.5 - Load Dependencies

In the first cell of the notebook, import our dependencies.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

figsize = (16,8)
```

We're also setting a shared variable `figsize` that we'll reuse later in our data visualization code.

### 0.6 - Load Dataset

In the next cell, load Vermont police stop data set into a Pandas dataframe.

```python
df_vt = pd.read_csv('./data/VT-clean.csv.gz', compression='gzip', low_memory=False)
```

> This command assumes that you are storing the data set in the `data` directory of the project.  If you are not, you can adjust the data file path accordingly.

# 1 - Vermont Police Data Exploration

Now begins the fun part.

### 1.0 - Preview the Available Data

We can get a quick preview of the first ten rows of the data set with the `head()` method.

```python
df_vt.head()
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>state</th>
      <th>stop_date</th>
      <th>stop_time</th>
      <th>location_raw</th>
      <th>county_name</th>
      <th>county_fips</th>
      <th>fine_grained_location</th>
      <th>police_department</th>
      <th>driver_gender</th>
      <th>driver_age_raw</th>
      <th>driver_age</th>
      <th>driver_race_raw</th>
      <th>driver_race</th>
      <th>violation_raw</th>
      <th>violation</th>
      <th>search_conducted</th>
      <th>search_type_raw</th>
      <th>search_type</th>
      <th>contraband_found</th>
      <th>stop_outcome</th>
      <th>is_arrested</th>
      <th>officer_id</th>
      <th>is_white</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>VT-2010-00001</td>
      <td>VT</td>
      <td>2010-07-01</td>
      <td>00:10</td>
      <td>East Montpelier</td>
      <td>Washington County</td>
      <td>50023.0</td>
      <td>COUNTY RD</td>
      <td>MIDDLESEX VSP</td>
      <td>M</td>
      <td>22.0</td>
      <td>22.0</td>
      <td>White</td>
      <td>White</td>
      <td>Moving Violation</td>
      <td>Moving violation</td>
      <td>False</td>
      <td>No Search Conducted</td>
      <td>N/A</td>
      <td>False</td>
      <td>Citation</td>
      <td>False</td>
      <td>-1.562157e+09</td>
      <td>True</td>
    </tr>
    <tr>
      <th>3</th>
      <td>VT-2010-00004</td>
      <td>VT</td>
      <td>2010-07-01</td>
      <td>00:11</td>
      <td>Whiting</td>
      <td>Addison County</td>
      <td>50001.0</td>
      <td>N MAIN ST</td>
      <td>NEW HAVEN VSP</td>
      <td>F</td>
      <td>18.0</td>
      <td>18.0</td>
      <td>White</td>
      <td>White</td>
      <td>Moving Violation</td>
      <td>Moving violation</td>
      <td>False</td>
      <td>No Search Conducted</td>
      <td>N/A</td>
      <td>False</td>
      <td>Arrest for Violation</td>
      <td>True</td>
      <td>-3.126844e+08</td>
      <td>True</td>
    </tr>
    <tr>
      <th>4</th>
      <td>VT-2010-00005</td>
      <td>VT</td>
      <td>2010-07-01</td>
      <td>00:35</td>
      <td>Hardwick</td>
      <td>Caledonia County</td>
      <td>50005.0</td>
      <td>i91 nb mm 62</td>
      <td>ROYALTON VSP</td>
      <td>M</td>
      <td>18.0</td>
      <td>18.0</td>
      <td>White</td>
      <td>White</td>
      <td>Moving Violation</td>
      <td>Moving violation</td>
      <td>False</td>
      <td>No Search Conducted</td>
      <td>N/A</td>
      <td>False</td>
      <td>Written Warning</td>
      <td>False</td>
      <td>9.225661e+08</td>
      <td>True</td>
    </tr>
    <tr>
      <th>5</th>
      <td>VT-2010-00006</td>
      <td>VT</td>
      <td>2010-07-01</td>
      <td>00:44</td>
      <td>Hardwick</td>
      <td>Caledonia County</td>
      <td>50005.0</td>
      <td>64000 I 91 N; MM64 I 91 N</td>
      <td>ROYALTON VSP</td>
      <td>F</td>
      <td>20.0</td>
      <td>20.0</td>
      <td>White</td>
      <td>White</td>
      <td>Vehicle Equipment</td>
      <td>Equipment</td>
      <td>False</td>
      <td>No Search Conducted</td>
      <td>N/A</td>
      <td>False</td>
      <td>Written Warning</td>
      <td>False</td>
      <td>-6.032327e+08</td>
      <td>True</td>
    </tr>
    <tr>
      <th>8</th>
      <td>VT-2010-00009</td>
      <td>VT</td>
      <td>2010-07-01</td>
      <td>01:10</td>
      <td>Rochester</td>
      <td>Windsor County</td>
      <td>50027.0</td>
      <td>36000 I 91 S; MM36 I 91 S</td>
      <td>ROCKINGHAM VSP</td>
      <td>M</td>
      <td>24.0</td>
      <td>24.0</td>
      <td>Black</td>
      <td>Black</td>
      <td>Moving Violation</td>
      <td>Moving violation</td>
      <td>False</td>
      <td>No Search Conducted</td>
      <td>N/A</td>
      <td>False</td>
      <td>Written Warning</td>
      <td>False</td>
      <td>2.939526e+08</td>
      <td>False</td>
    </tr>
  </tbody>
</table>

We can also list the available fields by reading the `columns` property.

```python
df_vt.columns
```

```text
Index(['id', 'state', 'stop_date', 'stop_time', 'location_raw', 'county_name',
       'county_fips', 'fine_grained_location', 'police_department',
       'driver_gender', 'driver_age_raw', 'driver_age', 'driver_race_raw',
       'driver_race', 'violation_raw', 'violation', 'search_conducted',
       'search_type_raw', 'search_type', 'contraband_found', 'stop_outcome',
       'is_arrested', 'officer_id'],
      dtype='object')
```


### 1.1 - Drop Missing Values

Let's do a quick count of each column to determine how consistantly filled-in the data is.

```python
df_vt.count()
```

```text
id                       283285
state                    283285
stop_date                283285
stop_time                283285
location_raw             282591
county_name              282580
county_fips              282580
fine_grained_location    282938
police_department        283285
driver_gender            281573
driver_age_raw           282114
driver_age               281999
driver_race_raw          279301
driver_race              278468
violation_raw            281107
violation                281107
search_conducted         283285
search_type_raw          281045
search_type                3419
contraband_found         283251
stop_outcome             280960
is_arrested              283285
officer_id               283273
dtype: int64
```

We can see that most columns have similar numbers of values besides "search type", which is not present for most of the rows, likely because most stops do not result in a search.

For our analysis, it will be best to have the exact same number of values for each field.  We'll go ahead now and make sure that every single cell has a value.

```python
# Fill missing search type values with placeholder
df_vt['search_type'].fillna('N/A', inplace=True)

# Drop rows with missing values
df_vt.dropna(inplace=True)
```

When we count the values again, we'll see that each column has the exact same number of entries.

```text
id                       273181
state                    273181
stop_date                273181
stop_time                273181
location_raw             273181
county_name              273181
county_fips              273181
fine_grained_location    273181
police_department        273181
driver_gender            273181
driver_age_raw           273181
driver_age               273181
driver_race_raw          273181
driver_race              273181
violation_raw            273181
violation                273181
search_conducted         273181
search_type_raw          273181
search_type              273181
contraband_found         273181
stop_outcome             273181
is_arrested              273181
officer_id               273181
dtype: int64
```

### 1.2 - Stops By County
Let's get a list of each county in the data set, along with how many traffic stops happened in each.

```python
df_vt['county_name'].value_counts()
```

```text
Windham County       37715
Windsor County       36464
Chittenden County    24815
Orange County        24679
Washington County    24633
Rutland County       22885
Addison County       22813
Bennington County    22250
Franklin County      19715
Caledonia County     16505
Orleans County       10344
Lamoille County       8604
Essex County          1239
Grand Isle County      520
Name: county_name, dtype: int64
```

If you're familiar with Vermont's geography, you'll notice that the police stops seem to be more concentrated in counties in the southern-half of the state.  The southern-half of the state is also where much of the cross-state traffic flows in transit to and from New Hampshire, Massachusetts, and New York state.  Since the traffic stop data is from the state troopers, this interstate traffic could potentially explain why we see more traffic stops in these counties.

https://public.tableau.com/views/VtPoliceStops/Sheet1?:embed=y&:display_count=yes&publish=yes

### 1.3 - Violations

We can also just as easily check out the distribution of traffic stop reasons.

```python
df_vt['violation_raw'].value_counts()
```

```text
Moving Violation              212100
Vehicle Equipment              50600
Externally Generated Stop       6160
Investigatory Stop              3608
Suspicion of DWI                 711
(Winooski) Mtr Vhc Vltn            1
(Winooski) Be On Look Rqst         1
Name: violation_raw, dtype: int64
```

Unsurprisingly, the top reason for a traffic stop is "Moving Violation" (speeding, reckless driving, etc.), followed by "Vehicle Equipment" (faulty lights, illegal modifications, etc.).  "Externally Generated Stop" and "Investigatory Stop" are both caused not by any fault in the driving behavior or vehicle, but on other information available to the officer.  "Suspicion of DWI" (driving while intoxicated) is surprisingly the least prevalent, with only 711 total recorded stops for this reason.

In order to keep the violation terms across counties and states, the team at Stanford normalized these terms in the `violation` column.

```python
df_vt['violation'].value_counts()
```

```text
Moving violation      212100
Equipment              50600
Other                   9768
DUI                      711
Other (non-mapped)         2
Name: violation, dtype: int64
```

We can see here that "Moving Violation", "Equipment", and "DUI" match the raw violation values 1:1, and "Externally Generated Stop" and "Investigatory Stop" have been consolidated into "Other".

### 1.4 - Outcomes

We can also examine the traffic stop outcomes.

```python
df_vt['stop_outcome'].value_counts()
```

```text
Written Warning         166488
Citation                103401
Arrest for Violation      3206
Warrant Arrest              76
Verbal Warning              10
Name: stop_outcome, dtype: int64
```

A majority of stops result in a written warning - which goes on the record but carries no direct penalty.  A bit over 1/3 of the stops result in a citation (commonly known as a ticket), which comes with a direct fine and can carry other negative side-effects such as raising a driver's auto insurance premiums.  The decision to give a warning or a citation is often mostly at the discretion of the police officer, so this could be a good source for studying bias.

### 1.5 - Stops By Gender
Let's break down the traffic stops by gender.

```python
df_vt['driver_gender'].value_counts()
```

```text
M    179678
F    101895
Name: driver_gender, dtype: int64
```

We can see that approximately 30% of the stops are of women drivers, and 70% are of men.

### 1.6 - Stops By Race

Let's also examine the distribution by race.

```python
df_vt['driver_race'].value_counts()
```

```text
White       266216
Black         5741
Asian         3607
Hispanic      2625
Other          279
Name: driver_race, dtype: int64
```

Most traffic stops are of white drivers, which is to be expected since [Vermont is around 94% white](https://www.census.gov/quickfacts/VT) (which makes it the 2nd-least diverse state in the nation, behind Maine).  Since white drivers make up approximately 94% of the traffic stops, there's no obvious bias here for pulling over non-white drivers vs white drivers.  Using the same methodology, however, we can also find that while black drivers make up roughly 2% of all traffic stops, [only 1.3% of Vermont's population is black](https://www.census.gov/quickfacts/VT).

Let's keep on analyzing the data to see what else we can learn.

### 1.7 - Police Stop Frequency by Race and Age

It would be interesting to visualize how the frequency of police stops breaks down by both race and age.

```python
fig, ax = plt.subplots()
ax.set_xlim(15, 70)
for race in df_vt['driver_race'].unique():
    s = df_vt[df_vt['driver_race'] == race]['driver_age']
    s.plot.kde(ax=ax, label=race)
ax.legend()
```

![Race Age Traffic Stop Distribution](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/race_age_dist.png)

We can see that young drivers in their late teens and early twenties are the most likely to be pulled over.  Between ages 25 and 35, the stop rate of each demographic drops off quickly. As far as the racial comparison goes, the most interesting disparity is that for white drivers between the ages of 35 and 50 the pull-over rate stay mostly consistant, whereas for other races it continues to drop steadily.

# 2 - Violation and Outcome Analysis

Now that we've got a feel for the dataset, we can start getting into some more advanced analysis.

One interesting topic that we touched on earlier is the fact that the decision to penalize a driver with a ticket or a citation is often at the discretion of the police officer.  With this in mind, let's see if there are any discernable patterns in driver demographics and stop outcome.

## 2.0 - Analysis Helper Function

In order to assist in this analysis, we'll define a helper function to aggregate a few important statistics from our dataset.

- `citations_per_warning` - The ratio of citations to warnings.
- `arrest_rate` - The percentage of stops that end in an arrest.

```python
def compute_outcome_stats(df):
    """Compute statistics regarding the relative quanties of arrests, warnings, and citations"""
    n_total = len(df)
    n_warnings = len(df[df['stop_outcome'] == 'Written Warning'])
    n_citations = len(df[df['stop_outcome'] == 'Citation'])
    n_arrests = len(df[df['stop_outcome'] == 'Arrest for Violation'])
    citations_per_warning = n_citations / n_warnings
    arrest_rate = n_arrests / n_total

    return(pd.Series(data = {
        'n_total': n_total,
        'n_warnings': n_warnings,
        'n_citations': n_citations,
        'n_arrests': n_arrests,
        'citations_per_warning': citations_per_warning,
        'arrest_rate': arrest_rate
    }))
```

Let's test out this helper function by applying it to the entire dataframe.

```python
compute_outcome_stats(df_vt)
```

```text
arrest_rate                   0.011721
citations_per_warning         0.620751
n_arrests                  3199.000000
n_citations              103270.000000
n_total                  272918.000000
n_warnings               166363.000000
dtype: float64
```

In the above result, we can see that about 1.2% of traffic stops result in an arrest, and there are on-average 0.62 citations (tickets) issued per warning.  This data passes the sanity check, but it's too coarse to tell us much so let's dig deeper.

## 2.1 - Breakdown By Gender

Using our helper function, along with Panda's [groupby](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html) method, we can easily compare these stats for male and female drivers.

```python
df_vt.groupby('driver_gender').apply(compute_outcome_stats)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>arrest_rate</th>
      <th>citations_per_warning</th>
      <th>n_arrests</th>
      <th>n_citations</th>
      <th>n_total</th>
      <th>n_warnings</th>
    </tr>
    <tr>
      <th>driver_gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>F</th>
      <td>0.007038</td>
      <td>0.548033</td>
      <td>697.0</td>
      <td>34805.0</td>
      <td>99036.0</td>
      <td>63509.0</td>
    </tr>
    <tr>
      <th>M</th>
      <td>0.014389</td>
      <td>0.665652</td>
      <td>2502.0</td>
      <td>68465.0</td>
      <td>173882.0</td>
      <td>102854.0</td>
    </tr>
  </tbody>
</table>

This is a simple example of the [split-apply-combine](https://pandas.pydata.org/pandas-docs/stable/groupby.html) pattern common in dataframe analyis.  We'll be building on this pattern for the remainder of the tutorial, so I reccomend that you make sure you understand how this comparision table is generated before continuing.

We can see here that men are, on average, twice as likely to be arrested during a traffic stop, and are also slightly more likely to be given a citation instead of a warning.  It is, ok course, not clear from the data whether this is indicative of any bias by the police officers, or if it just reflects that men are being pulled over for more serious offenses than women on average.

## 2.2 - Breakdown By Race

Let's now compute the same comparison, grouping by race.

```python
df_vt.groupby('driver_race').apply(compute_outcome_stats)
```

```text
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>arrest_rate</th>
      <th>citations_per_warning</th>
      <th>n_arrests</th>
      <th>n_citations</th>
      <th>n_total</th>
      <th>n_warnings</th>
    </tr>
    <tr>
      <th>driver_race</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Asian</th>
      <td>0.006384</td>
      <td>1.002339</td>
      <td>22.0</td>
      <td>1714.0</td>
      <td>3446.0</td>
      <td>1710.0</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.019925</td>
      <td>0.802379</td>
      <td>111.0</td>
      <td>2428.0</td>
      <td>5571.0</td>
      <td>3026.0</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.016393</td>
      <td>0.865827</td>
      <td>42.0</td>
      <td>1168.0</td>
      <td>2562.0</td>
      <td>1349.0</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.011571</td>
      <td>0.611188</td>
      <td>3024.0</td>
      <td>97960.0</td>
      <td>261339.0</td>
      <td>160278.0</td>
    </tr>
  </tbody>
</table>
```

Ok, this is interesting.  We can see that Asian drivers are arrested at the lowest rate, but receive tickets at the highest rate (roughly 1 ticket per warning).  Black and Hispanic drivers are both arrested at a higher rate and ticketed at a higher rate than white drivers.

Let's visualize this result as a bar chart.

```python
race_agg = df_vt.groupby(['driver_race']).apply(compute_outcome_stats)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=figsize)
race_agg['citations_per_warning'].plot.barh(ax=axes[0], figsize=figsize, title="Citation Rate By Race")
race_agg['arrest_rate'].plot.barh(ax=axes[1], figsize=figsize, title='Arrest Rate By Race')
```

![Citations and arrests by race and violation](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/citations_and_arrests_by_race.png)

This is getting more interesting.

## 2.2 - Group By Outcome and Violation

Let's deepen our analysis by grouping each statistic by the violation that catalyzed the traffic stop.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>arrest_rate</th>
      <th>citations_per_warning</th>
      <th>n_arrests</th>
      <th>n_citations</th>
      <th>n_total</th>
      <th>n_warnings</th>
    </tr>
    <tr>
      <th>driver_race</th>
      <th>violation</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="4" valign="top">Asian</th>
      <th>DUI</th>
      <td>0.200000</td>
      <td>0.333333</td>
      <td>2.0</td>
      <td>2.0</td>
      <td>10.0</td>
      <td>6.0</td>
    </tr>
    <tr>
      <th>Equipment</th>
      <td>0.006270</td>
      <td>0.132143</td>
      <td>2.0</td>
      <td>37.0</td>
      <td>319.0</td>
      <td>280.0</td>
    </tr>
    <tr>
      <th>Moving violation</th>
      <td>0.005563</td>
      <td>1.183190</td>
      <td>17.0</td>
      <td>1647.0</td>
      <td>3056.0</td>
      <td>1392.0</td>
    </tr>
    <tr>
      <th>Other</th>
      <td>0.016393</td>
      <td>0.875000</td>
      <td>1.0</td>
      <td>28.0</td>
      <td>61.0</td>
      <td>32.0</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Black</th>
      <th>DUI</th>
      <td>0.200000</td>
      <td>0.142857</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>10.0</td>
      <td>7.0</td>
    </tr>
    <tr>
      <th>Equipment</th>
      <td>0.029181</td>
      <td>0.220651</td>
      <td>26.0</td>
      <td>156.0</td>
      <td>891.0</td>
      <td>707.0</td>
    </tr>
    <tr>
      <th>Moving violation</th>
      <td>0.016052</td>
      <td>0.942385</td>
      <td>71.0</td>
      <td>2110.0</td>
      <td>4423.0</td>
      <td>2239.0</td>
    </tr>
    <tr>
      <th>Other</th>
      <td>0.048583</td>
      <td>2.205479</td>
      <td>12.0</td>
      <td>161.0</td>
      <td>247.0</td>
      <td>73.0</td>
    </tr>
    <tr>
      <th rowspan="4" valign="top">Hispanic</th>
      <th>DUI</th>
      <td>0.200000</td>
      <td>3.000000</td>
      <td>2.0</td>
      <td>6.0</td>
      <td>10.0</td>
      <td>2.0</td>
    </tr>
    <tr>
      <th>Equipment</th>
      <td>0.023560</td>
      <td>0.187898</td>
      <td>9.0</td>
      <td>59.0</td>
      <td>382.0</td>
      <td>314.0</td>
    </tr>
    <tr>
      <th>Moving violation</th>
      <td>0.012422</td>
      <td>1.058824</td>
      <td>26.0</td>
      <td>1062.0</td>
      <td>2093.0</td>
      <td>1003.0</td>
    </tr>
    <tr>
      <th>Other</th>
      <td>0.064935</td>
      <td>1.366667</td>
      <td>5.0</td>
      <td>41.0</td>
      <td>77.0</td>
      <td>30.0</td>
    </tr>
    <tr>
      <th rowspan="5" valign="top">White</th>
      <th>DUI</th>
      <td>0.192364</td>
      <td>0.455026</td>
      <td>131.0</td>
      <td>172.0</td>
      <td>681.0</td>
      <td>378.0</td>
    </tr>
    <tr>
      <th>Equipment</th>
      <td>0.012233</td>
      <td>0.190486</td>
      <td>599.0</td>
      <td>7736.0</td>
      <td>48965.0</td>
      <td>40612.0</td>
    </tr>
    <tr>
      <th>Moving violation</th>
      <td>0.008635</td>
      <td>0.732720</td>
      <td>1747.0</td>
      <td>84797.0</td>
      <td>202321.0</td>
      <td>115729.0</td>
    </tr>
    <tr>
      <th>Other</th>
      <td>0.058378</td>
      <td>1.476672</td>
      <td>547.0</td>
      <td>5254.0</td>
      <td>9370.0</td>
      <td>3558.0</td>
    </tr>
    <tr>
      <th>Other (non-mapped)</th>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>2.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>

Ok, this table looks interesting, but it's rather large and overwhelming.  Let's trim down that dataset in order to just retrieve the most important information.

```python
# Create new column to represent whether the driver is white
df_vt['is_white'] = df_vt['driver_race'] == 'White'

# Remove violation with too few data points
df_vt_filtered = df_vt[~df_vt['violation'].isin(['Other (non-mapped)', 'DUI'])]
```

We're creating a new column, that could be used instead of `driver_race`, that just represents whether or not the driver is white.  We are also generating a filtered version of the dataframe, that stips out the two violation types with the fewest datapoints.

> We not assigning the filtered dataframe to `df_vt` since we'll want to keep using the complete unfilted dataset in the next sections.

Let's redo our race + violation aggregation now, using our refined dataset.

```python
df_vt_filtered.groupby(['is_white','violation']).apply(compute_outcome_stats).to_html().replace('\n','')
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>arrest_rate</th>
      <th>citations_per_warning</th>
      <th>n_arrests</th>
      <th>n_citations</th>
      <th>n_total</th>
      <th>n_warnings</th>
    </tr>
    <tr>
      <th>is_white</th>
      <th>violation</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="3" valign="top">False</th>
      <th>Equipment</th>
      <td>0.023241</td>
      <td>0.193697</td>
      <td>37.0</td>
      <td>252.0</td>
      <td>1592.0</td>
      <td>1301.0</td>
    </tr>
    <tr>
      <th>Moving violation</th>
      <td>0.011910</td>
      <td>1.039922</td>
      <td>114.0</td>
      <td>4819.0</td>
      <td>9572.0</td>
      <td>4634.0</td>
    </tr>
    <tr>
      <th>Other</th>
      <td>0.046753</td>
      <td>1.703704</td>
      <td>18.0</td>
      <td>230.0</td>
      <td>385.0</td>
      <td>135.0</td>
    </tr>
    <tr>
      <th rowspan="3" valign="top">True</th>
      <th>Equipment</th>
      <td>0.012233</td>
      <td>0.190486</td>
      <td>599.0</td>
      <td>7736.0</td>
      <td>48965.0</td>
      <td>40612.0</td>
    </tr>
    <tr>
      <th>Moving violation</th>
      <td>0.008635</td>
      <td>0.732720</td>
      <td>1747.0</td>
      <td>84797.0</td>
      <td>202321.0</td>
      <td>115729.0</td>
    </tr>
    <tr>
      <th>Other</th>
      <td>0.058378</td>
      <td>1.476672</td>
      <td>547.0</td>
      <td>5254.0</td>
      <td>9370.0</td>
      <td>3558.0</td>
    </tr>
  </tbody>
</table>

In the above table, we can see that non-white drivers are more likely to be arrested during a stop that was initiated due to an equipment or moving violation, but white drivers are more likely to be arrest for a traffic stop resulting from an "other" reason.  Non-white drivers are also, to varying degrees, more likely to be tickets for each of the violations thank white drivers.

Let's generate a bar chart now in order to visualize this data broken down by race.
```python
race_stats = df_vt_filtered.groupby(['violation', 'driver_race']).apply(compute_outcome_stats).unstack()
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
race_stats.plot.bar(y='arrest_rate', ax=axes[0], title='Arrest Rate By Race and Violation')
race_stats.plot.bar(y='citations_per_warning', ax=axes[1], title='Citations Per Warning By Race and Violation')
```

![citations and arrests by race and violation](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/citations_and_arrests_by_race_and_violation.png)

We can see in this chart that Black drivers are more likely, across the board, to be issued a citation than white drivers, and Hispanic and Black drivers are generally arrested at a higher rate that white drivers, except for in the "other" category.  Asian drivers are arrested at very low rates, but their citation rates are all over the place.

Using the above code, we can easily create a similar visualization for grouping by gender.

```python
gender_stats = df_vt_filtered.groupby(['violation','driver_gender']).apply(compute_outcome_stats).unstack()
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
ax_gender_arrests = gender_stats.plot.bar(y='arrest_rate', ax=axes[0], title='Arrests By Gender and Violation', figsize=figsize)
ax_gender_citations = gender_stats.plot.bar(y='citations_per_warning', ax=axes[1], title='Citations By Gender and Violation', figsize=figsize)
```

![citations and arrests by gender and violation](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/citations_and_arrests_by_gender_and_violation.png)

In the above figure, we can see that the gender-based trends that we observed earlier are fairly consistent across violation types.

These results on the stop reasons and outcomes are compelling, and are suggestive of potential racial bias, but they are too inconsistent across violation types to provide any definitive answers.  Let's dig deeper to see what else we can find.

# 3 - Search Outcome Analysis

Two of the more interesting fields available to us are `search_conducted` and `contraband_found`.

In the analysis by the "Standford Open Policing Project", they use these two fields to perform what is known as an "outcome test".

On the [project website](https://openpolicing.stanford.edu/findings/), the "outcome test" is described as such -
"In the 1950s, the Nobel prize-winning economist Gary Becker proposed an elegant method to test for bias in search decisions: the outcome test.

Becker proposed looking at search outcomes. If officers don’t discriminate, he argued, they should find contraband — like illegal drugs or weapons — on searched minorities at the same rate as on searched whites. If searches of minorities turn up contraband at lower rates than searches of whites, the outcome test suggests officers are applying a double standard, searching minorities on the basis of less evidence."

The authors of the project also make the point that only using the "hit rate", or the rate of searches where contraband is found, can be misleading.  For this reason we'll also want to use the "search rate" in our analysis - the rate a which a traffic stop results in a search.

We'll now use the available data to perform our own outcome test, to determine whether minorities in Vermont are searched on the basis of less evidence than white drivers.

### Compute Search Rate and Hit Rate

We'll define a new function to compute the search rate and hit rate for the traffic stops in our dataframe.

- Search Rate - The rate at which a traffic stop results in a search.  I.e. a search rate of `0.20` would signify that out of 100 traffic stops, 20 resulted in a search on average.
- Hit Rate - The rate at which contraband is found in a search. I.e. a hit rate of `0.80` would signify that out of 100 searches, 80 searches resulted in contraband (drugs, unregistered weapons, etc.) being found.

```python
def compute_search_stats(df):
    """Compute the search rate and hit rate"""
    search_conducted = df['search_conducted']
    contraband_found = df['contraband_found']
    n_stops     = len(search_conducted)
    n_searches  = sum(search_conducted)
    n_hits      = sum(contraband_found)

    if (n_stops) < 50:
        search_rate = None
    else:
        search_rate = n_searches / n_stops

    if (n_searches) < 5:
        hit_rate = None
    else:
        hit_rate = n_hits / n_searches

    return(pd.Series(data = {
        'n_stops': n_stops,
        'n_searches': n_searches,
        'n_hits': n_hits,
        'search_rate': search_rate,
        'hit_rate': hit_rate
    }))
```

### Compute Search Stats For Entire Dataset

We can test our new function to determine the search rate and hit rate for the entire state.

```python
compute_search_stats(df_vt)
```

hit_rate            0.796865
n_hits           2593.000000
n_searches       3254.000000
n_stops        272918.000000
search_rate         0.011923
dtype: float64

Here we can see that each traffic stop had a 1.2% change of resulting in a search, and each search had an 80% chance of yielding contraband.

### Compare Search Stats By Driver Gender

Using the Pandas `groupby` method, we can compute how the search stats differ by gender.

```python
df_vt.groupby('driver_gender').apply(compute_search_stats)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>hit_rate</th>
      <th>n_hits</th>
      <th>n_searches</th>
      <th>n_stops</th>
      <th>search_rate</th>
    </tr>
    <tr>
      <th>driver_gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>F</th>
      <td>0.789392</td>
      <td>506.0</td>
      <td>641.0</td>
      <td>99036.0</td>
      <td>0.006472</td>
    </tr>
    <tr>
      <th>M</th>
      <td>0.798699</td>
      <td>2087.0</td>
      <td>2613.0</td>
      <td>173882.0</td>
      <td>0.015027</td>
    </tr>
  </tbody>
</table>

We can see here that men are about three times as likely to be searched as women, but that for each gender the same standard of evidence is used, since roughly 80% of searches for both result in contraband being found.  The implication here is men are searched and caught with contraband more often than women, but that there is no discernable gender discrimination in deciding who to search.

### Compare Search Stats By Age

We can split the dataset into age buckets and perform the same analysis.

```python
age_groups = pd.cut(df_vt["driver_age"], np.arange(15, 70, 5))
df_vt.groupby(age_groups).apply(compute_search_stats)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>hit_rate</th>
      <th>n_hits</th>
      <th>n_searches</th>
      <th>n_stops</th>
      <th>search_rate</th>
    </tr>
    <tr>
      <th>driver_age</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>(15, 20]</th>
      <td>0.847988</td>
      <td>569.0</td>
      <td>671.0</td>
      <td>27418.0</td>
      <td>0.024473</td>
    </tr>
    <tr>
      <th>(20, 25]</th>
      <td>0.838000</td>
      <td>838.0</td>
      <td>1000.0</td>
      <td>43275.0</td>
      <td>0.023108</td>
    </tr>
    <tr>
      <th>(25, 30]</th>
      <td>0.788462</td>
      <td>492.0</td>
      <td>624.0</td>
      <td>34759.0</td>
      <td>0.017952</td>
    </tr>
    <tr>
      <th>(30, 35]</th>
      <td>0.766756</td>
      <td>286.0</td>
      <td>373.0</td>
      <td>27746.0</td>
      <td>0.013443</td>
    </tr>
    <tr>
      <th>(35, 40]</th>
      <td>0.742991</td>
      <td>159.0</td>
      <td>214.0</td>
      <td>23203.0</td>
      <td>0.009223</td>
    </tr>
    <tr>
      <th>(40, 45]</th>
      <td>0.692913</td>
      <td>88.0</td>
      <td>127.0</td>
      <td>24055.0</td>
      <td>0.005280</td>
    </tr>
    <tr>
      <th>(45, 50]</th>
      <td>0.575472</td>
      <td>61.0</td>
      <td>106.0</td>
      <td>24103.0</td>
      <td>0.004398</td>
    </tr>
    <tr>
      <th>(50, 55]</th>
      <td>0.706667</td>
      <td>53.0</td>
      <td>75.0</td>
      <td>22517.0</td>
      <td>0.003331</td>
    </tr>
    <tr>
      <th>(55, 60]</th>
      <td>0.833333</td>
      <td>30.0</td>
      <td>36.0</td>
      <td>17502.0</td>
      <td>0.002057</td>
    </tr>
    <tr>
      <th>(60, 65]</th>
      <td>0.500000</td>
      <td>6.0</td>
      <td>12.0</td>
      <td>12514.0</td>
      <td>0.000959</td>
    </tr>
  </tbody>
</table>

We can see here that the search rate steadily declines as drivers get older.  What also interesting is that the hit rate also declines rapidly older drivers.  This shows that older drivers are searched less often, and searches on older drivers generally turn up contraband more rarely.

It's worth noting that the sample sizes (`n_hits`, `n_searches`, and `n_stops`) also decrease steadily through the age brackets, resulting in values that are less precise and much more volatile.  This increase in volatility possibly explains why the hit rates on individuals aged 50-60 are significantly higher than in the neighboring age brackets.

### Compare Search Stats By Race

Now for the most interesting part - comparing search data by race.

```python
df_vt.groupby('driver_race').apply(compute_search_stats)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>hit_rate</th>
      <th>n_hits</th>
      <th>n_searches</th>
      <th>n_stops</th>
      <th>search_rate</th>
    </tr>
    <tr>
      <th>driver_race</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Asian</th>
      <td>0.785714</td>
      <td>22.0</td>
      <td>28.0</td>
      <td>3446.0</td>
      <td>0.008125</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.686620</td>
      <td>195.0</td>
      <td>284.0</td>
      <td>5571.0</td>
      <td>0.050978</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.644231</td>
      <td>67.0</td>
      <td>104.0</td>
      <td>2562.0</td>
      <td>0.040593</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.813601</td>
      <td>2309.0</td>
      <td>2838.0</td>
      <td>261339.0</td>
      <td>0.010859</td>
    </tr>
  </tbody>
</table>

Black and Hispanic drivers are searched at much higher rates than white drivers (5% and 4% of traffic stops respectively, versus 1% for white drivers), but the searches of these drivers only yield contraband 60-70% of the time, compared to 80% of the time for white drivers.

To rephrase these results - Black drivers are 500% more likely to be searched than white drivers during a traffic stop, but are 20% less likely to be caught with contraband in the event of a search.

### Compare Search Stats By Race and Location

Let's add in location as another factor.  It's possible that some counties (such as those with interstate highways where opioid trafficking is prevalent) have a much higher search rate / lower hit rates for both white and non-white drivers, leading to distortion in the overall stats.  By controlling for location, we can determine if this is the case.

We'll define a two new helper functions to generate the visualizations.

```python
def generate_comparison_scatter(df, ax, state, race, field):
    """Generate scatter plot comparing field for white drivers with minority drivers"""
    race_location_agg = df.groupby(['county_name','driver_race']).apply(compute_search_stats).reset_index().dropna()
    race_location_agg = race_location_agg.pivot(index='county_name', columns='driver_race', values=field)
    ax = race_location_agg.plot.scatter(ax=ax, x='White', y=race, s=150)
    ax.set_xlabel('{} - White'.format(field, ))
    ax.set_ylabel('{} - {}'.format(field, race))
    ax.set_title("{} By County - {}".format(field, state))
    lim = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    diag_line, = ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c=".3")
    return ax

def generate_comparison_scatters(df, state):
    """Generate scatter plots comparing search rates of white drivers with black and hispanic drivers"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 16))
    generate_comparison_scatter(df, axes[0][0], state, 'Black', 'search_rate')
    generate_comparison_scatter(df, axes[0][1], state, 'Hispanic', 'search_rate')
    generate_comparison_scatter(df, axes[1][0], state, 'Black', 'hit_rate')
    generate_comparison_scatter(df, axes[1][1], state, 'Hispanic', 'hit_rate')
    return fig
```

We can now generate the scatter plots using the `generate_comparison_scatters` function.

```python
generate_comparison_scatters(df_vt, 'VT')
```

![search scatters vt](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_vt.png)


The plots above are comparing `search_rate` (top row) and `hit_rate` (bottom row) for Black (left column) and Hispanic (right column) drivers compared with white drivers in each county.  If all of the dots (each of which represents a county) followed the diagonal center line, the implication would be that white drivers and non-white drivers are searched with the exact same standard of evidence.

Unfortunately, this is not the case.  In the above charts, we can see that, for every single county, the search rate is higher for minorities and the hit rate is lower.

Let's define one more visualization helper function, to show all of these results on the same scatter plot.

```python
def generate_county_search_stats_scatter(df, state):
    """Generate a scatter plot of search rate vs. hit rate by race and county"""
    race_location_agg = df.groupby(['county_name','driver_race']).apply(compute_search_stats)

    fig, ax = plt.subplots(figsize=figsize)
    for c, frame in race_location_agg.groupby('driver_race'):
        ax.scatter(x=frame['hit_rate'], y=frame['search_rate'], s=150, label=c)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fancybox=True)
    ax.set_xlabel('Hit Rate')
    ax.set_ylabel('Search Rate')
    ax.set_title("Search Stats By County and Race - {}".format(state))
    return fig
```

```python
generate_county_search_stats_scatter(df_vt, "VT")
```

**In the above visualization, we can see a clear pattern of discrimination in traffic stop searches.**

The search rates and hit rates for white drivers in most counties are quite consistently clustered around 80% and 1% respectively.  We can see, however, that nearly every county searches black and hispanic drivers at a higher rate, and that these searches uniformally have a lower hit rate than those on white drivers.

This state-wide pattern of a higher search rate combined with a lower hit rate suggests that a lower standard of evidence is used when deciding to search black and hispanic drivers compared to when searching white drivers.

You've heard the phrase "A picture is worth a thousand words"?  The above chart is one of those pictures - and the name of the picture is "Systemic Racism".

> You might notice that only one county is represented for Asian drivers - this is due to the lack of data for searches of Asian drivers in other counties.

# 3 - Analyzing Other States

### 3.0 - Massachuesstts
Let's now perform the same analysis on my home state, Massachusetts.  This time we'll have more data to work with - roughly 3.4 million traffic stops.

Download the dataset to your project's `/data` directory - https://stacks.stanford.edu/file/druid:py883nd2578/MA-clean.csv.gz

Then load the dataset (this time we'll only load the columns that we're examining, in order to save memory), and remove rows with missing data.
```python
df_ma = pd.read_csv('./data/MA-clean.csv.gz', compression='gzip', low_memory=False, usecols=fields)
df_ma.dropna(inplace=True)
df_ma = df_ma[df_ma['driver_race'] != 'Other']
```

Let's generate a statewide table of search rate and hit rate by race.

```python
df_ma.groupby('driver_race').apply(compute_search_stats)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>hit_rate</th>
      <th>n_hits</th>
      <th>n_searches</th>
      <th>n_stops</th>
      <th>search_rate</th>
    </tr>
    <tr>
      <th>driver_race</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Asian</th>
      <td>0.331169</td>
      <td>357.0</td>
      <td>1078.0</td>
      <td>101942.0</td>
      <td>0.010575</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.487150</td>
      <td>4170.0</td>
      <td>8560.0</td>
      <td>350498.0</td>
      <td>0.024422</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.449502</td>
      <td>5007.0</td>
      <td>11139.0</td>
      <td>337782.0</td>
      <td>0.032977</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.523037</td>
      <td>18220.0</td>
      <td>34835.0</td>
      <td>2527393.0</td>
      <td>0.013783</td>
    </tr>
  </tbody>
</table>

We can see here again that Black and Hispanic drivers are searched at significantly higher rates than white drivers. The differences in hit rates are not as extreme as in Vermont, but they are still noticeably lower for Black and Hispanic drivers than for whites.  Asian drivers, interestingly, are the least likely to be searched and also the least likely to have contraband if they are searched.

If we compare the stats for MA to VT, we'll also notice that police in MA seem to use a much lower standard of evidence when searching a vehicle, with their searches averaging around 50% hit rate, compared to 80% in VT.

Let's generate the scatter plots too, to examine these stats visually.

```python
generate_comparison_scatters(df_ma, 'MA')
generate_county_search_stats_scatter(df_ma, "MA")
```

![search scatters ma](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_ma.png)
![county scatters ma](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/county_scatters_ma.png)

The trend here is much less obvious than in Vermont, but it's still clear that traffic stops of minority drivers tend to be more likely to result in a search, even though the hit rates are *generally* lower than they are for white drivers.

### 3.1 - Wisconsin

Wisconsin has caught quite a bit of flack recently for being "a bad place to live if you're not white" (include news articles).

Let's see how their police stats stack up.

Again, you'll need to download the Wisconsin dataset to your project's `/data` directory - https://stacks.stanford.edu/file/druid:py883nd2578/WI-clean.csv.gz


```python
df_wi = pd.read_csv('./data/WI-clean.csv.gz', compression='gzip', low_memory=False, usecols=fields)
df_wi.dropna(inplace=True)
df_wi = df_wi[df_wi['driver_race'] != 'Other']
```

We'll again compute the search stats using our handy helper method.

```python
df_wi.groupby('driver_race').apply(compute_search_stats)
```

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>hit_rate</th>
      <th>n_hits</th>
      <th>n_searches</th>
      <th>n_stops</th>
      <th>search_rate</th>
    </tr>
    <tr>
      <th>driver_race</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Asian</th>
      <td>0.470817</td>
      <td>121.0</td>
      <td>257.0</td>
      <td>24577.0</td>
      <td>0.010457</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.477574</td>
      <td>1299.0</td>
      <td>2720.0</td>
      <td>56050.0</td>
      <td>0.048528</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.415741</td>
      <td>449.0</td>
      <td>1080.0</td>
      <td>35210.0</td>
      <td>0.030673</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.526300</td>
      <td>5103.0</td>
      <td>9696.0</td>
      <td>778227.0</td>
      <td>0.012459</td>
    </tr>
  </tbody>
</table>

The trends here should be starting to look familiar.  White drivers in Wisconsin are much less likely to be searched than non-white drivers (aside from Asians, who tend to be searched at the same rate as whites).  Despite the much higher search rates, searches of non-white drivers are, again, actually less likely on average to yield contraband than searches on white drivers.

We'll visualize the same result, by county, in our scatterplots.

```python
generate_comparison_scatters(df_wi, 'WI')
generate_county_search_stats_scatter(df_wi, "WI")
```

![search scatters wi](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_wi.png)
![county scatters wi](https://storage.googleapis.com/cdn.patricktriest.com/blog/images/posts/policing-data/county_scatters_wi.png)

Starting to look familiar?  We can see in the chart bellow that the standard of evidence for searching non-white drivers is higher in virtually every county than for white drivers.  In one outlying county, almost 25% (!) of traffic stops for black drivers resulted in a search, even though only 50% of those searches yielded contraband.

< change this section a bit >

# 5 - What next?

Does this mean we shouldnt support our police departments? Does it mean that most police officers are overtly racist?  **Certainly not.**

Does it mean that in the United States, non-white citizens are uniformly searched with a lower standard of evidence than white citizens?  **Yes**.

Regardless of political views, I think everyone can agree that *facts are paramount to idealogy* in making laws and setting policy.  These numbers don't lie - this data was sourced directly from the state police departments, and the examples that we've gone over here have not been cherry picked to make any political point: these trends are apparent across the entire dataset of 60 million police stops.  To see the full analysis for all 20 available states, check out the official findings here - https://5harad.com/papers/traffic-stops.pdf.

[ include extra stats from the official findings - ticket rates, tail lights, marajuana ]

Whatever your views may be on the divisive social and political issues that have enveloped our country over the past few years, I think it's important to take a step back and to look objectively at what is shown by the data.  I'm not suggesting any solutions here, that's really not the point of this blog post, but I sincerely believe that sensibly acknowledging the problem across political lines is the first step to any sustainable long-term progress.

I hope that this tutorial has provided the tools you might need to take the analysis further.  There's a *lot* more that you can do with the data than what we've covered here.

- Analyze police stops for your home state and county (if the data is available).
- Expand the analysis to include other factors in the dataset, such as `Stop Reason` and `Search Type`.  The data sets for some states have lots of additional fields available as well, such as whether the stop was drug related, whether the driver was from out-of-state, and metadata covering the year, make, and model of the car.
- Combine your analysis with US census data on the demographic, social, and economic data about each county.
- Create a web app to display the county trends on an interactive map.
- Build a mobile app to warn drivers when they're entering a county that seems to be more distrusting of drivers of a certain race.
- Open-source your own analysis, spread your findings, seek out peer review, maybe even write an explanatory blog post.

As always, feel free to commend below with any questions, comments, or criticisms.