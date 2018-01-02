## Data Science, Politics, and Police

The intersection of science, politics, personal opinion, and social policy can be rather complex.  This junction of ideas and disciplines is often rife with controversies, strongly held viewpoints, and agendas that are often [more based on belief than on empirical evidence](https://en.wikipedia.org/wiki/Global_warming_controversy).  Data science is particularly important in this area since it provides a methodology for examining the world in a pragmatic fact-first manner, and is capable of providing insight into some of the most important issues that we face today.

The recent high-profile police shootings of unarmed black men, such as [Michael Brown](https://en.wikipedia.org/wiki/Shooting_of_Michael_Brown) (2014), [Tamir Rice](https://en.wikipedia.org/wiki/Shooting_of_Tamir_Rice) (2014), [Anton Sterling](https://en.wikipedia.org/wiki/Shooting_of_Alton_Sterling) (2016), and [Philando Castile](https://en.wikipedia.org/wiki/Shooting_of_Philando_Castile) (2016), have triggered a divisive national dialog on the issue of racial bias in policing.

These shootings have spurred the growth of large social movements seeking to raise awareness of what is viewed as the systemic targeting of people-of-color by police forces across the country.  On the other side of the political spectrum, many hold a view that the unbalanced targeting of non-white citizens is a myth created by the media based on a handful of extreme cases, and that these highly-publicized stories are not representative of the national norm.

In June 2017, a team of researchers at Stanford University collected and released an open-source data set of 60 million state police patrol stops from 20 states across the US.  In this tutorial, we will walk through how to analyze and visualize this data using Python.

![county scatters vt](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_VT.png)

The source code and figures for this analysis can be found in the companion Github repository - https://github.com/triestpa/Police-Analysis-Python

To preview the completed IPython notebook, visit the page [here](https://github.com/triestpa/Police-Analysis-Python/blob/master/traffic_stop_analysis.ipynb).

> This tutorial and analysis would not be possible without the work performed by [The Standford Open Policing Project](https://openpolicing.stanford.edu/).  Much of the analysis performed in this tutorial is based on the work that has already performed by this team.  [A short tutorial](https://openpolicing.stanford.edu/tutorials/) for working with the data using the R programming language is provided on the official project website.

## The Data

In the United States there are more than 50,000 traffic stops on a typical day.  The potential number of data points for each stop is huge, from the demographics (age, race, gender) of the driver, to the location, time of day, stop reason, stop outcome, car model, and much more.  Unfortunately, not every state makes this data available, and those that do often have different standards for which information is reported.  Different counties and districts within each state can also be inconstant in how each traffic stop is recorded.  The [research team at Stanford](https://openpolicing.stanford.edu/) has managed to gather traffic-stop data from twenty states, and has worked to regularize the reporting standards for 11 fields.

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

## 0 - Getting Started

We'll start with analyzing the data set for Vermont.  We're looking at Vermont first for a few reasons.

1. The Vermont dataset is small enough to be very manageable and quick to operate on, with only 283,285 traffic stops (compared to the Texas data set, for instance, which contains almost 24 million records).
1. There is not much missing data, as all eleven fields mentioned above are covered.
1. Vermont is 94% white, but is also in a part of the country known for being very liberal (disclaimer - I grew up in the Boston area, and I've spent a quite a bit of time in Vermont).  Many in this area consider this state to be very progressive and might like to believe that their state institutions are not as prone to systemic racism as the institutions in other parts of the country.  It will be interesting to determine if the data validates this view.

#### 0.0 - Download Datset

First, download the Vermont traffic stop data - https://stacks.stanford.edu/file/druid:py883nd2578/VT-clean.csv.gz

#### 0.1 - Setup Project

Create a new directory for the project, say `police-data-analysis`, and move the downloaded file into a `/data` directory within the project.

#### 0.2 - Optional: Create new virtualenv (or Anaconda) environment

If you want to keep your Python dependencies neat and separated between projects, now would be the time to create and activate a new environment for this analysis, using either [virtualenv](https://virtualenv.pypa.io/en/stable/) or [Anaconda](https://conda.io/docs/user-guide/install/index.html).

Here are some tutorials to help you get set up.
virtualenv - https://virtualenv.pypa.io/en/stable/
Anaconda - https://conda.io/docs/user-guide/install/index.html

#### 0.3 - Install dependencies

We'll need to install a few Python packages to perform our analysis.

On the command line, run the following command to install the required libraries.
```bash
pip install numpy pandas matplotlib ipython jupyter
```

> If you're using Anaconda, you can replace the `pip` command here with `conda`.  Also, depending on your installation, you might need to use `pip3` instead of `pip` in order to install the Python 3 versions of the packages.

#### 0.4 - Start Jupyter Notebook

Start a new local Jupyter notebook server from the command line.

```bash
jupyter notebook
```

Open your browser to the specified URL (probably `localhost:8888`, unless you have a special configuration) and create a new notebook.

> I used Python 3.6 for writing this tutorial.  If you want to use another Python version, that's fine, most of the code that we'll cover should work on any Python 2.x or 3.x distribution.

#### 0.5 - Load Dependencies

In the first cell of the notebook, import our dependencies.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

figsize = (16,8)
```

We're also setting a shared variable `figsize` that we'll reuse later on in our data visualization logic.

#### 0.6 - Load Dataset

In the next cell, load Vermont police stop data set into a [Pandas dataframe](https://pandas.pydata.org/pandas-docs/stable/dsintro.html#dataframe).

```python
df_vt = pd.read_csv('./data/VT-clean.csv.gz', compression='gzip', low_memory=False)
```

> This command assumes that you are storing the data set in the `data` directory of the project.  If you are not, you can adjust the data file path accordingly.

## 1 - Vermont Data Exploration

Now begins the fun part.

#### 1.0 - Preview the Available Data

We can get a quick preview of the first ten rows of the data set with the `head()` method.

```python
df_vt.head()
```

<table border="0" class="dataframe">
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

<br>

#### 1.1 - Drop Missing Values

Let's do a quick count of each column to determine how consistently populated the data is.

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

We can see that most columns have similar numbers of values besides `search_type`, which is not present for most of the rows, likely because most stops do not result in a search.

For our analysis, it will be best to have the exact same number of values for each field.  We'll go ahead now and make sure that every single cell has a value.

```python
# Fill missing search type values with placeholder
df_vt['search_type'].fillna('N/A', inplace=True)

# Drop rows with missing values
df_vt.dropna(inplace=True)

df_vt.count()
```

<br>

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

<br>

#### 1.2 - Stops By County
Let's get a list of all counties in the data set, along with how many traffic stops happened in each.

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

If you're familiar with Vermont's geography, you'll notice that the police stops seem to be more concentrated in counties in the southern-half of the state.  The southern-half of the state is also where much of the cross-state traffic flows in transit to and from New Hampshire, Massachusetts, and New York.  Since the traffic stop data is from the state troopers, this interstate highway traffic could potentially explain why we see more traffic stops in these counties.

Here's a quick map generated with [Tableau](https://public.tableau.com/profile/patrick.triest#!/vizhome/VtPoliceStops/Sheet1) to visualize this regional distribution.

![Vermont County Map](https://cdn.patricktriest.com/blog/images/posts/policing-data/vermont_map.png)

#### 1.3 - Violations

We can also check out the distribution of traffic stop reasons.

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

Unsurprisingly, the top reason for a traffic stop is `Moving Violation` (speeding, reckless driving, etc.), followed by `Equipment` (faulty lights, illegal modifications, etc.).

By using the `violation_raw` fields as reference, we can see that the `Other` category includes "Investigatory Stop" (the police have reason to suspect that the driver of the vehicle has committed a crime) and  "Externally Generated Stop" (possibly as a result of a 911 call, or a referral from municipal police departments).

`DUI` ("driving under the influence", i.e. drunk driving) is surprisingly the least prevalent, with only 711 total recorded stops for this reason over the five year period (2010-2015) that the dataset covers.  This seems low, since [Vermont had 2,647 DUI arrests in 2015](http://www.statisticbrain.com/number-of-dui-arrests-per-state/), so I suspect that a large proportion of these arrests were performed by municipal police departments, and/or began with a `Moving Violation` stop, instead of a more specific `DUI` stop.

#### 1.4 - Outcomes

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

A majority of stops result in a written warning - which goes on the record but carries no direct penalty.  A bit over 1/3 of the stops result in a citation (commonly known as a ticket), which comes with a direct fine and can carry other negative side-effects such as raising a driver's auto insurance premiums.

The decision to give a warning or a citation is often at the discretion of the police officer, so this could be a good source for studying bias.

#### 1.5 - Stops By Gender
Let's break down the traffic stops by gender.

```python
df_vt['driver_gender'].value_counts()
```

```text
M    179678
F    101895
Name: driver_gender, dtype: int64
```

We can see that approximately 36% of the stops are of women drivers, and 64% are of men.

#### 1.6 - Stops By Race

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

Most traffic stops are of white drivers, which is to be expected since [Vermont is around 94% white](https://www.census.gov/quickfacts/VT) (making it the 2nd-least diverse state in the nation, [behind Maine](https://www.census.gov/quickfacts/ME)).  Since white drivers make up approximately 94% of the traffic stops, there's no obvious bias here for pulling over non-white drivers vs white drivers.  Using the same methodology, however, we can also see that while black drivers make up roughly 2% of all traffic stops, [only 1.3% of Vermont's population is black](https://www.census.gov/quickfacts/VT).

Let's keep on analyzing the data to see what else we can learn.

#### 1.7 - Police Stop Frequency by Race and Age

It would be interesting to visualize how the frequency of police stops breaks down by both race and age.

```python
fig, ax = plt.subplots()
ax.set_xlim(15, 70)
for race in df_vt['driver_race'].unique():
    s = df_vt[df_vt['driver_race'] == race]['driver_age']
    s.plot.kde(ax=ax, label=race)
ax.legend()
```

![Race Age Traffic Stop Distribution](https://cdn.patricktriest.com/blog/images/posts/policing-data/race_age_dist.png)

We can see that young drivers in their late teens and early twenties are the most likely to be pulled over.  Between ages 25 and 35, the stop rate of each demographic drops off quickly. As far as the racial comparison goes, the most interesting disparity is that for white drivers between the ages of 35 and 50 the pull-over rate stays mostly flat, whereas for other races it continues to drop steadily.

## 2 - Violation and Outcome Analysis

Now that we've got a feel for the dataset, we can start getting into some more advanced analysis.

One interesting topic that we touched on earlier is the fact that the decision to penalize a driver with a ticket or a citation is often at the discretion of the police officer.  With this in mind, let's see if there are any discernable patterns in driver demographics and stop outcome.

#### 2.0 - Analysis Helper Function

In order to assist in this analysis, we'll define a helper function to aggregate a few important statistics from our dataset.

- `citations_per_warning` - The ratio of citations to warnings.  A higher number signifies a greater likelihood of being ticketed instead of getting off with a warning.
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

In the above result, we can see that about `1.17%` of traffic stops result in an arrest, and there are on-average `0.62` citations (tickets) issued per warning.  This data passes the sanity check, but it's too coarse to provide many interesting insights.  Let's dig deeper.

#### 2.1 - Breakdown By Gender

Using our helper function, along with the Pandas dataframe [groupby](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.groupby.html) method, we can easily compare these stats for male and female drivers.

```python
df_vt.groupby('driver_gender').apply(compute_outcome_stats)
```

<table border="0" class="dataframe">
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

This is a simple example of the common [split-apply-combine](https://pandas.pydata.org/pandas-docs/stable/groupby.html) technique.  We'll be building on this pattern for the remainder of the tutorial, so make sure that you understand how this comparison table is generated before continuing.

We can see here that men are, on average, twice as likely to be arrested during a traffic stop, and are also slightly more likely to be given a citation than women.  It is, of course, not clear from the data whether this is indicative of any bias by the police officers, or if it reflects that men are being pulled over for more serious offenses than women on average.

#### 2.2 - Breakdown By Race

Let's now compute the same comparison, grouping by race.

```python
df_vt.groupby('driver_race').apply(compute_outcome_stats)
```

<table border="0" class="dataframe">
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

Ok, this is interesting.  We can see that Asian drivers are arrested at the lowest rate, but receive tickets at the highest rate (roughly 1 ticket per warning).  Black and Hispanic drivers are both arrested at a higher rate and ticketed at a higher rate than white drivers.

Let's visualize these results.

```python
race_agg = df_vt.groupby(['driver_race']).apply(compute_outcome_stats)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=figsize)
race_agg['citations_per_warning'].plot.barh(ax=axes[0], figsize=figsize, title="Citation Rate By Race")
race_agg['arrest_rate'].plot.barh(ax=axes[1], figsize=figsize, title='Arrest Rate By Race')
```

![Citations and arrests by race and violation](https://cdn.patricktriest.com/blog/images/posts/policing-data/citations_and_arrests_by_race.png)

#### 2.3 - Group By Outcome and Violation

We'll deepen our analysis by grouping each statistic by the violation that triggered the traffic stop.

```python
df_vt.groupby(['driver_race','violation']).apply(compute_outcome_stats)
```

<table border="0" class="dataframe">
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

Ok, well this table looks interesting, but it's rather large and visually overwhelming.  Let's trim down that dataset in order to retrieve a more focused subset of information.

```python
# Create new column to represent whether the driver is white
df_vt['is_white'] = df_vt['driver_race'] == 'White'

# Remove violation with too few data points
df_vt_filtered = df_vt[~df_vt['violation'].isin(['Other (non-mapped)', 'DUI'])]
```

We're generating a new column to represent whether or not the driver is white.  We are also generating a filtered version of the dataframe that strips out the two violation types with the fewest datapoints.

> We not assigning the filtered dataframe to `df_vt` since we'll want to keep using the complete unfiltered dataset in the next sections.

Let's redo our race + violation aggregation now, using our filtered dataset.

```python
df_vt_filtered.groupby(['is_white','violation']).apply(compute_outcome_stats)
```

<table border="0" class="dataframe">
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

Ok great, this is much easier to read.

In the above table, we can see that non-white drivers are more likely to be arrested during a stop that was initiated due to an equipment or moving violation, but white drivers are more likely to be arrested for a traffic stop resulting from "Other" reasons.  Non-white drivers are more likely than white drivers to be given tickets for each violation.

#### 2.4 - Visualize Stop Outcome and Violation Results

Let's generate a bar chart now in order to visualize this data broken down by race.
```python
race_stats = df_vt_filtered.groupby(['violation', 'driver_race']).apply(compute_outcome_stats).unstack()
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
race_stats.plot.bar(y='arrest_rate', ax=axes[0], title='Arrest Rate By Race and Violation')
race_stats.plot.bar(y='citations_per_warning', ax=axes[1], title='Citations Per Warning By Race and Violation')
```

![citations and arrests by race and violation](https://cdn.patricktriest.com/blog/images/posts/policing-data/citations_and_arrests_by_race_and_violation.png)

We can see in these charts that Hispanic and Black drivers are generally arrested at a higher rate than white drivers (with the exception of the rather ambiguous "Other" category). and  that Black drivers are more likely, across the board, to be issued a citation than white drivers.  Asian drivers are arrested at very low rates, and their citation rates are highly variable.

These results are compelling, and are suggestive of potential racial bias, but they are too inconsistent across violation types to provide any definitive answers.  Let's dig deeper to see what else we can find.

## 3 - Search Outcome Analysis

Two of the more interesting fields available to us are `search_conducted` and `contraband_found`.

In the analysis by the "Standford Open Policing Project", they use these two fields to perform what is known as an "outcome test".

On the [project website](https://openpolicing.stanford.edu/findings/), the "outcome test" is summarized clearly.

> In the 1950s, the Nobel prize-winning economist Gary Becker proposed an elegant method to test for bias in search decisions: the outcome test.
>
> Becker proposed looking at search outcomes. If officers don’t discriminate, he argued, they should find contraband — like illegal drugs or weapons — on searched minorities at the same rate as on searched whites. If searches of minorities turn up contraband at lower rates than searches of whites, the outcome test suggests officers are applying a double standard, searching minorities on the basis of less evidence."

[Findings, Stanford Open Policing Project](https://openpolicing.stanford.edu/findings/)

The authors of the project also make the point that only using the "hit rate", or the rate of searches where contraband is found, can be misleading.  For this reason, we'll also need to use the "search rate" in our analysis - the rate at which a traffic stop results in a search.

We'll now use the available data to perform our own outcome test, in order to determine whether minorities in Vermont are routinely searched on the basis of less evidence than white drivers.

#### 3.0 Compute Search Rate and Hit Rate

We'll define a new function to compute the search rate and hit rate for the traffic stops in our dataframe.

- **Search Rate** - The rate at which a traffic stop results in a search.  A search rate of `0.20` would signify that out of 100 traffic stops, 20 resulted in a search.
- **Hit Rate** - The rate at which contraband is found in a search. A hit rate of `0.80` would signify that out of 100 searches, 80 searches resulted in contraband (drugs, unregistered weapons, etc.) being found.

```python
def compute_search_stats(df):
    """Compute the search rate and hit rate"""
    search_conducted = df['search_conducted']
    contraband_found = df['contraband_found']
    n_stops     = len(search_conducted)
    n_searches  = sum(search_conducted)
    n_hits      = sum(contraband_found)

    # Filter out counties with too few stops
    if (n_stops) < 50:
        search_rate = None
    else:
        search_rate = n_searches / n_stops

    # Filter out counties with too few searches
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

<br>

#### 3.1 - Compute Search Stats For Entire Dataset

We can test our new function to determine the search rate and hit rate for the entire state.

```python
compute_search_stats(df_vt)
```

```text
hit_rate            0.796865
n_hits           2593.000000
n_searches       3254.000000
n_stops        272918.000000
search_rate         0.011923
dtype: float64
```

Here we can see that each traffic stop had a 1.2% change of resulting in a search, and each search had an 80% chance of yielding contraband.

#### 3.2 - Compare Search Stats By Driver Gender

Using the Pandas `groupby` method, we can compute how the search stats differ by gender.

```python
df_vt.groupby('driver_gender').apply(compute_search_stats)
```

<table border="0" class="dataframe">
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

We can see here that men are three times as likely to be searched as women, and that 80% of searches for both genders resulted in contraband being found.  The data shows that men are searched and caught with contraband more often than women, but it is unclear whether there is any gender discrimination in deciding who to search since the hit rate is equal.

#### 3.3 - Compare Search Stats By Age

We can split the dataset into age buckets and perform the same analysis.

```python
age_groups = pd.cut(df_vt["driver_age"], np.arange(15, 70, 5))
df_vt.groupby(age_groups).apply(compute_search_stats)
```

<table border="0" class="dataframe">
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

We can see here that the search rate steadily declines as drivers get older, and that the hit rate also declines rapidly for older drivers.

#### 3.4 - Compare Search Stats By Race

Now for the most interesting part - comparing search data by race.

```python
df_vt.groupby('driver_race').apply(compute_search_stats)
```

<table border="0" class="dataframe">
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

Black and Hispanic drivers are searched at much higher rates than White drivers (5% and 4% of traffic stops respectively, versus 1% for white drivers), but the searches of these drivers only yield contraband 60-70% of the time, compared to 80% of the time for White drivers.

Let's rephrase these results.

*Black drivers are **500% more likely** to be searched than white drivers during a traffic stop, but are **13% less likely** to be caught with contraband in the event of a search.*

*Hispanic drivers are **400% more likely** to be searched than white drivers during a traffic stop, but are **17% less likely** to be caught with contraband in the event of a search.*

#### 3.5 - Compare Search Stats By Race and Location

Let's add in location as another factor.  It's possible that some counties (such as those with larger towns or with interstate highways where opioid trafficking is prevalent) have a much higher search rate / lower hit rates for both white and non-white drivers, but also have greater racial diversity, leading to distortion in the overall stats.  By controlling for location, we can determine if this is the case.

We'll define three new helper functions to generate the visualizations.

```python
def generate_comparison_scatter(df, ax, state, race, field, color):
    """Generate scatter plot comparing field for white drivers with minority drivers"""
    race_location_agg = df.groupby(['county_fips','driver_race']).apply(compute_search_stats).reset_index().dropna()
    race_location_agg = race_location_agg.pivot(index='county_fips', columns='driver_race', values=field)
    ax = race_location_agg.plot.scatter(ax=ax, x='White', y=race, s=150, label=race, color=color)
    return ax

def format_scatter_chart(ax, state, field):
    """Format and label to scatter chart"""
    ax.set_xlabel('{} - White'.format(field))
    ax.set_ylabel('{} - Non-White'.format(field, race))
    ax.set_title("{} By County - {}".format(field, state))
    lim = max(ax.get_xlim()[1], ax.get_ylim()[1])
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    diag_line, = ax.plot(ax.get_xlim(), ax.get_ylim(), ls="--", c=".3")
    ax.legend()
    return ax

def generate_comparison_scatters(df, state):
    """Generate scatter plots comparing search rates of white drivers with black and hispanic drivers"""
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
    generate_comparison_scatter(df, axes[0], state, 'Black', 'search_rate', 'red')
    generate_comparison_scatter(df, axes[0], state, 'Hispanic', 'search_rate', 'orange')
    generate_comparison_scatter(df, axes[0], state, 'Asian', 'search_rate', 'green')
    format_scatter_chart(axes[0], state, 'Search Rate')

    generate_comparison_scatter(df, axes[1], state, 'Black', 'hit_rate', 'red')
    generate_comparison_scatter(df, axes[1], state, 'Hispanic', 'hit_rate', 'orange')
    generate_comparison_scatter(df, axes[1], state, 'Asian', 'hit_rate', 'green')
    format_scatter_chart(axes[1], state, 'Hit Rate')

    return fig
```

We can now generate the scatter plots using the `generate_comparison_scatters` function.

```python
generate_comparison_scatters(df_vt, 'VT')
```

![search scatters vt](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_VT.png)

The plots above are comparing `search_rate` (left) and `hit_rate` (right) for minority drivers compared with white drivers in each county.  If all of the dots (each of which represents the stats for a single county and race) followed the diagonal center line, the implication would be that white drivers and non-white drivers are searched at the exact same rate with the exact same standard of evidence.

Unfortunately, this is not the case.  In the above charts, we can see that, for every county, the search rate is higher for Black and Hispanic drivers even though the hit rate is lower.

Let's define one more visualization helper function, to show all of these results on a single scatter plot.

```python
def generate_county_search_stats_scatter(df, state):
    """Generate a scatter plot of search rate vs. hit rate by race and county"""
    race_location_agg = df.groupby(['county_fips','driver_race']).apply(compute_search_stats)

    colors = ['blue','orange','red', 'green']
    fig, ax = plt.subplots(figsize=figsize)
    for c, frame in race_location_agg.groupby('driver_race'):
        ax.scatter(x=frame['hit_rate'], y=frame['search_rate'], s=150, label=c, color=colors.pop())
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=4, fancybox=True)
    ax.set_xlabel('Hit Rate')
    ax.set_ylabel('Search Rate')
    ax.set_title("Search Stats By County and Race - {}".format(state))
    return fig
```

```python
generate_county_search_stats_scatter(df_vt, "VT")
```

![county scatters vt](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_VT.png)

As the old idiom goes - *a picture is worth a thousand words*.  The above chart is one of those pictures - and the name of the picture is "Systemic Racism".

The search rates and hit rates for white drivers in most counties are consistently clustered around 80% and 1% respectively.  We can see, however, that nearly every county searches Black and Hispanic drivers at a higher rate, and that these searches uniformly have a lower hit rate than those on White drivers.

This state-wide pattern of a higher search rate combined with a lower hit rate suggests that a lower standard of evidence is used when deciding to search Black and Hispanic drivers compared to when searching White drivers.

> You might notice that only one county is represented by Asian drivers - this is due to the lack of data for searches of Asian drivers in other counties.

## 4 - Analyzing Other States

Vermont is a great state to test out our analysis on, but the dataset size is relatively small.  Let's now perform the same analysis on other states to determine if this pattern persists across state lines.

#### 4.0 - Massachusetts

First we'll generate the analysis for my home state, Massachusetts.  This time we'll have more data to work with - roughly 3.4 million traffic stops.

Download the dataset to your project's `/data` directory - https://stacks.stanford.edu/file/druid:py883nd2578/MA-clean.csv.gz

We've developed a solid reusable formula for reading and visualizing each state's dataset, so let's wrap the entire recipe in a new helper function.

```python
fields = ['county_fips', 'driver_race', 'search_conducted', 'contraband_found']
types = {
    'contraband_found': bool,
    'county_fips': float,
    'driver_race': object,
    'search_conducted': bool
}

def analyze_state_data(state):
    df = pd.read_csv('./data/{}-clean.csv.gz'.format(state), compression='gzip', low_memory=True, dtype=types, usecols=fields)
    df.dropna(inplace=True)
    df = df[df['driver_race'] != 'Other']
    generate_comparison_scatters(df, state)
    generate_county_search_stats_scatter(df, state)
    return df.groupby('driver_race').apply(compute_search_stats)
```

We're making a few optimizations here in order to make the analysis a bit more streamlined and computationally efficient.  By only reading the four columns that we're interested in, and by specifying the datatypes ahead of time, we'll be able to read larger datasets into memory more quickly.

```python
analyze_state_data('MA')
```

The first output is a statewide table of search rate and hit rate by race.

<table border="0" class="dataframe">
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

We can see here again that Black and Hispanic drivers are searched at significantly higher rates than white drivers. The differences in hit rates are not as extreme as in Vermont, but they are still noticeably lower for Black and Hispanic drivers than for White drivers.  Asian drivers, interestingly, are the least likely to be searched and also the least likely to have contraband if they are searched.

![search scatters MA](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_MA.png)
![county scatters MA](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_MA.png)

If we compare the stats for MA to VT, we'll also notice that police in MA seem to use a much lower standard of evidence when searching a vehicle, with their searches averaging around a 50% hit rate, compared to 80% in VT.

The trend here is much less obvious than in Vermont, but it is still clear that traffic stops of Black and Hispanic drivers are more likely to result in a search, despite the fact the searches of White drivers are more likely to result in contraband being found.

#### 4.1 - Wisconsin & Connecticut

Wisconsin and Connecticut have been named as some of the [worst states in America for racial disparities](https://www.wpr.org/wisconsin-considered-one-worst-states-racial-disparities).  Let's see how their police stats stack up.

Again, you'll need to download the Wisconsin and Connecticut dataset to your project's `/data` directory.

- Wisconsin: https://stacks.stanford.edu/file/druid:py883nd2578/WI-clean.csv.gz
- Connecticut: https://stacks.stanford.edu/file/druid:py883nd2578/CT-clean.csv.gz

We can call our `analyze_state_data` function for Wisconsin once the dataset has been downloaded.
```python
analyze_state_data('WI')
```

<table border="0" class="dataframe">
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

The trends here are starting to look familiar.  White drivers in Wisconsin are much less likely to be searched than non-white drivers (aside from Asians, who tend to be searched at around the same rates as whites).  Searches of non-white drivers are, again, less likely to yield contraband than searches on white drivers.

![search scatters WI](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_WI.png)
![county scatters WI](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_WI.png)

We can see here, yet again, that the standard of evidence for searching Black and Hispanic drivers is lower in virtually every county than for White drivers.  In one outlying county, almost 25% (!) of traffic stops for Black drivers resulted in a search, even though only half of those searches yielded contraband.

Let's do the same analysis for Connecticut

```python
analyze_state_data('CT')
```

<table border="0" class="dataframe">
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
      <td>0.384615</td>
      <td>10.0</td>
      <td>26.0</td>
      <td>5949.0</td>
      <td>0.004370</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.284072</td>
      <td>346.0</td>
      <td>1218.0</td>
      <td>37460.0</td>
      <td>0.032515</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.291925</td>
      <td>282.0</td>
      <td>966.0</td>
      <td>31154.0</td>
      <td>0.031007</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.379344</td>
      <td>1179.0</td>
      <td>3108.0</td>
      <td>242314.0</td>
      <td>0.012826</td>
    </tr>
  </tbody>
</table>

![search scatters CT](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_CT.png)
![county scatters CT](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_CT.png)

Again, the pattern persists.

#### 4.2 - Arizona

We can generate each result rather quickly for each state (with available data), once we've downloaded each dataset.

```python
analyze_state_data('AZ')
```

<table border="0" class="dataframe">
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
      <td>0.196664</td>
      <td>224.0</td>
      <td>1139.0</td>
      <td>48177.0</td>
      <td>0.023642</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.255548</td>
      <td>2188.0</td>
      <td>8562.0</td>
      <td>116795.0</td>
      <td>0.073308</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.160930</td>
      <td>5943.0</td>
      <td>36929.0</td>
      <td>501619.0</td>
      <td>0.073620</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.242564</td>
      <td>9288.0</td>
      <td>38291.0</td>
      <td>1212652.0</td>
      <td>0.031576</td>
    </tr>
  </tbody>
</table>

![search scatters AZ](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_AZ.png)
![county scatters AZ](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_AZ.png)

#### 4.3 - Colorado

```python
analyze_state_data('CO')
```

<table border="0" class="dataframe">
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
      <td>0.537634</td>
      <td>50.0</td>
      <td>93.0</td>
      <td>32471.0</td>
      <td>0.002864</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.481283</td>
      <td>270.0</td>
      <td>561.0</td>
      <td>71965.0</td>
      <td>0.007795</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.450454</td>
      <td>1041.0</td>
      <td>2311.0</td>
      <td>308499.0</td>
      <td>0.007491</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.651388</td>
      <td>3638.0</td>
      <td>5585.0</td>
      <td>1767804.0</td>
      <td>0.003159</td>
    </tr>
  </tbody>
</table>

![search scatters CO](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_CO.png)
![county scatters CO](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_CO.png)


#### 4.4 - Washington

```python
analyze_state_data('WA')
```

<table border="0" class="dataframe">
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
      <td>0.087143</td>
      <td>608.0</td>
      <td>6977.0</td>
      <td>352063.0</td>
      <td>0.019817</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.130799</td>
      <td>1717.0</td>
      <td>13127.0</td>
      <td>254577.0</td>
      <td>0.051564</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.103366</td>
      <td>2128.0</td>
      <td>20587.0</td>
      <td>502254.0</td>
      <td>0.040989</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.156008</td>
      <td>15768.0</td>
      <td>101072.0</td>
      <td>4279273.0</td>
      <td>0.023619</td>
    </tr>
  </tbody>
</table>

![search scatters WA](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_WA.png)
![county scatters WA](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_WA.png)


#### 4.5 - North Carolina

```python
analyze_state_data('NC')
```

<table border="0" class="dataframe">
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
      <td>0.104377</td>
      <td>31.0</td>
      <td>297.0</td>
      <td>46287.0</td>
      <td>0.006416</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.182489</td>
      <td>1955.0</td>
      <td>10713.0</td>
      <td>1222533.0</td>
      <td>0.008763</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.119330</td>
      <td>776.0</td>
      <td>6503.0</td>
      <td>368878.0</td>
      <td>0.017629</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.153850</td>
      <td>3387.0</td>
      <td>22015.0</td>
      <td>3146302.0</td>
      <td>0.006997</td>
    </tr>
  </tbody>
</table>

![search scatters NC](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_NC.png)
![county scatters NC](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_NC.png)

#### 4.6 - Texas

You might want to let this one run while you go fix yourself a cup of coffee or tea.  At almost 24 million traffic stops, the Texas dataset takes a rather long time to process.

```python
analyze_state_data('TX')
```

<table border="0" class="dataframe">
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
      <td>0.289271</td>
      <td>976.0</td>
      <td>3374.0</td>
      <td>349105.0</td>
      <td>0.009665</td>
    </tr>
    <tr>
      <th>Black</th>
      <td>0.345983</td>
      <td>27588.0</td>
      <td>79738.0</td>
      <td>2300427.0</td>
      <td>0.034662</td>
    </tr>
    <tr>
      <th>Hispanic</th>
      <td>0.219449</td>
      <td>37080.0</td>
      <td>168969.0</td>
      <td>6525365.0</td>
      <td>0.025894</td>
    </tr>
    <tr>
      <th>White</th>
      <td>0.335098</td>
      <td>83157.0</td>
      <td>248157.0</td>
      <td>13576726.0</td>
      <td>0.018278</td>
    </tr>
  </tbody>
</table>

![search scatters TX](https://cdn.patricktriest.com/blog/images/posts/policing-data/search_scatters_TX.png)
![county scatters TX](https://cdn.patricktriest.com/blog/images/posts/policing-data/county_scatter_TX.png)

#### 4.7 - Even more data visualizations

I highly recommend that you visit the [Standford Open Policing Project results page](https://openpolicing.stanford.edu/findings/) for more visualizations of this data.  Here you can browse the search outcome results for all available states, and explore additional analysis that the researchers have performed such as stop rate by race (using county population demographics data) as well as the effects of recreational marijuana legalization on search rates.

## 5 - What next?

Do these results imply that police officers are overtly racist?  **No.**

Do they show that Black and Hispanic drivers are searched much more frequently than white drivers, often with a lower standard of evidence?  **Yes.**

What we are observing here appears to be a pattern of systemic racism.  The racial disparities revealed in this analysis are a reflection of an entrenched mistrust of certain minorities in the United States.  The data and accompanying analysis are indicative of social trends that are certainly not limited to police officers, and *should not be used to disparage this profession as a whole*.  Racial discrimination is present at all levels of society from [retail stores](https://www.theguardian.com/us-news/2015/jun/22/zara-reports-culture-of-favoritism-based-on-race) to the [tech industry](https://www.wired.com/story/tech-leadership-race-problem/) to [academia](https://www.scientificamerican.com/article/sex-and-race-discrimination-in-academia-starts-even-before-grad-school/).

We are able to empirically identify these trends only because state police deparments (and the Open Policing team at Stanford) have made this data available to the public; no similar datasets exist for most other professions and industries.  Releasing datasets about these issues is commendable (but sadly still somewhat uncommon, especially in the private sector) and will help to further identify where these disparities exist, and to influence policies in order to provide a fair, effective way to counteract these biases.

To see the full official analysis for all 20 available states, check out the official findings paper here - https://5harad.com/papers/traffic-stops.pdf.

I hope that this tutorial has provided the tools you might need to take this analysis further.  There's a *lot* more that you can do with the data than what we've covered here.

- Analyze police stops for your home state and county (if the data is available).  If the data is not available, submit a formal request to your local representatives and institutions that the data be made public.
- Combine your analysis with US census data on the demographic, social, and economic stats about each county.
- Create a web app to display the county trends on an interactive map.
- Build a mobile app to warn drivers when they're entering an area that appears to be more distrusting of drivers of a certain race.
- Open-source your own analysis, spread your findings, seek out peer review, maybe even write an explanatory blog post.

The source code and figures for this analysis can be found in the companion Github repository - https://github.com/triestpa/Police-Analysis-Python

To view the completed IPython notebook, visit the page [here](https://github.com/triestpa/Police-Analysis-Python/blob/master/traffic_stop_analysis.ipynb).

The code for this project is 100% open source ([MIT license](https://github.com/triestpa/Police-Analysis-Python/blob/master/LICENSE)), so feel free to use it however you see fit in your own projects.

As always, please feel free to comment below with any questions, comments, or criticisms.
