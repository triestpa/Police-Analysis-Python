# Intro

Policing has become an increasingly divisive issue over the past few years in American public discourse.

The seemingly unending high-profile police shootings of unarmed black men (such as Michael Brown, Tamir Rice, Anton Sterling, and Philando Castile) have catalyzed massive protests against what is seen as a systemic, and often violent, targeting of people-of-color by police forces across the country.

On the other side of the political spectrum, a common belief is that the unbalanced police targeting of non-white citizens is a myth created by the mainstream media based on a handful of extreme cases that are not representative of the national norm.

In June 2017, a team of researchers at Stanford University collected and released an open-source data set of 60 million state police patrol stops from 20 states across the US.  In this tutorial, we walk through how analyze and visualize this data using Python, and we'll work to cut through the political smoke-screens in order to quantitatively determine the existence of systemic racially driven policing bias.

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

1. The Vermont dataset is small enough to be very manageable, at only 283,285 traffic stops (compared to the Texas data set, for instance, which contains records on almost 24 million stops).
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
pip install numpy pandas matplotlib jupyter plotly
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

import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected=True)
```

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

< Insert table here! >

We can also just list the available fields by reading the `columns` property.

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

### 1.1 - Stops By County
Let's get a list of each county in the data set, along with how many traffic stops happened in each.

```python
df_vt['county_name'].value_counts()
```

```text
Windham County       38160
Windsor County       37096
Chittenden County    26571
Washington County    25974
Orange County        25463
Rutland County       23940
Addison County       23756
Bennington County    22651
Franklin County      20184
Caledonia County     17177
Orleans County       10617
Lamoille County       9094
Essex County          1359
Grand Isle County      538
Name: county_name, dtype: int64
```

If you're familiar with Vermont's geography, you'll notice that the police stops seem to be more concentrated in counties in the southern-half of the state.  The southern-half of the state is also where much of the cross-state traffic flows in transit to and from New Hampshire, Massachusetts, and New York state.  Since the traffic stop data is from the state troopers, this interstate traffic could potentially explain why we see more traffic stops in these counties.

https://public.tableau.com/views/VtPoliceStops/Sheet1?:embed=y&:display_count=yes&publish=yes


### 1.2 - Stops By Gender
We can also break down the traffic stops by gender.

```python
df_vt['driver_gender'].value_counts()
```

```text
M    179678
F    101895
Name: driver_gender, dtype: int64
```

We can see that approximately 30% of the stops are of women drivers, and 70% are of men.

### 1.3 - Stops By Race

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

Most traffic stops are of white drivers, which is expected since Vermont is around 94% white (which makes it the 2nd-least diverse state in the nation, behind Maine).  Since white drivers make up approximately 94% of the traffic stops, it would appear that the there is no observable statewide bias for pulling over non-white drivers vs. white drivers.

We're far from done, however.  Let's keep on analyzing the data to see what else we can learn.

### 1.4 - Drop Missing Values

Let's do a quick count of each column to see if we're missing much data.

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

We can see that most columns have similar numbers of values besides "search type", which is not present for almost all stops, likely because most stops do not result in a search.

When we're doing an analysis on a dataset, it's best to have the exact same number of values for each field.  We'll go ahead now and drop the stops that have missing data.

```python
# Drop rows with missing values for important fields
df_vt['search_conducted'].dropna(inplace=True)
df_vt['contraband_found'].dropna(inplace=True)
df_vt['county_name'].dropna(inplace=True)
df_vt['driver_age'].dropna(inplace=True)
df_vt['driver_race'].dropna(inplace=True)
df_vt['driver_gender'].dropna(inplace=True)

df_vt['search_type'].fillna('N/A', inplace=True)
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


### 1.5 - Police Stop Frequency By Age

### 1.6 - Police Stop Frequency by Race and Age

It would be more interesting to see how the frequency of police stops breaks down by both race and age.

```python
fig, ax = plt.subplots()
ax.set_xlim(15, 70)
for race in df_vt['driver_race'].unique():
    s = df_vt[df_vt['driver_race'] == race]['driver_age']
    s.plot.kde(ax=ax, label=race)
ax.legend()
```

< insert chart>

We can see that young drivers in their late teens and early twenties are the most likely to be pulled over.  Between ages 25 and 35, the stop rate of each demographic drops off quickly. The most interesting disparity is that it plateaus, and even rises a bit for white drivers between the ages of 35 and 50, whereas for other races it continues to drop steadily.

# 2 - Search Outcome Analysis

Now that we have a feel for the dataset, and that it's been cleaned up a bit, we can start getting into some more advanced analysis.

Two of the more interesting fields available to us are `search_conducted` and `contraband_found`.

In the analysis by the "Standford Open Policing Project", they use these two fields to perform what is known as an "outcome test".

"In the 1950s, the Nobel prize-winning economist Gary Becker proposed an elegant method to test for bias in search decisions: the outcome test.

Becker proposed looking at search outcomes. If officers don’t discriminate, he argued, they should find contraband — like illegal drugs or weapons — on searched minorities at the same rate as on searched whites. If searches of minorities turn up contraband at lower rates than searches of whites, the outcome test suggests officers are applying a double standard, searching minorities on the basis of less evidence." - https://openpolicing.stanford.edu/findings/

We'll now use the available data to perform our own outcome test, to determine whether minorities in Vermont are searched on the basis of less evidence than white drivers.

### 2.0 - Compute Search Rate and Hit Rate

We'll define a new function to compute the search rate and hit rate for the traffic stops in our dataframe.

- Search Rate - The rate at which a traffic stop results in a search.  I.e. a search rate of `0.20` would signify that out of 100 traffic stops, 20 resulted in a search on average.
- Hit Rate - The rate at which contraband is found in a search. I.e. a hit rate of `0.80` would signify that out of 100 searches, 80 searches resulted in contraband (drugs, unregistered weapons, etc.) being found.

```python
def compute_hit_rate(df):
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

    return(pd.DataFrame(data = {
        'n_stops': n_stops,
        'n_searches': n_searches,
        'n_hits': n_hits,
        'search_rate': search_rate,
        'hit_rate': hit_rate
    }, index=[0]))
```

### 2.1 - Compute Search Stats For Entire Dataset

We can test our new function to determine the search rate and hit rate for the entire state.

```python
compute_search_stats(df_vt)
```

< insert result table >

Here we can see that each traffic stop had a 1.2% change of resulting in a search, and each search had an 80% chance of yielding contraband.

### 2.2 - Compare Search Stats By Driver Gender

Using the Pandas `groupby` method, we can compute how the search stats differ by gender.

```python
df_vt.groupby('driver_gender').apply(compute_search_stats)
```

< insert chart >

We can see here that men are about three times as likely to be searched as women, but that for each gender the same standard of evidence is used, since roughly 80% of searches for both result in contraband being found.  The implication here is men are searched and caught with contraband more often than women, but that there is no discernable gender discrimination in deciding who to search.

### 2.3 - Compare Search Stats By Age

We can split the dataset into age buckets and perform the same analysis.

```python
age_groups = pd.cut(df_vt["driver_age"], np.arange(15, 70, 5))
df_vt.groupby(age_groups).apply(compute_search_stats)
```

< insert chart >

We can see here that, as we observed prior, the search rate steadily declines as drivers get older.  What is more interesting, however, is that the hit rate also declines rapidly older drivers.  What this means is that older drivers are searched less often, and searches on older drivers generally turn up contraband more rarely.

It's worth noting that the sample sizes (`n_hits`, `n_searches`, and `n_stops`) also decrease steadily through the age brackets, resulting in values that are less precise and much more volatile.  This drop in sample size probably explains why the hit rates on individuals aged 55-60 are much higher than in the neighboring age brackets (I also would like to imagine that this could be a reflection of the midlife crisis hippy crowd who retire to Vermont in a psychedelic VW minibus packed with the "Grateful Dead" discography and a pound of dope).

### 2.4 - Compare Search Stats By Race

Now for the most interesting part - comparing search data by race.

```python
df_vt.groupby('driver_race').apply(compute_search_stats)
```

< insert table >

Black and hispanic drivers are searched at higher rates than white drivers (5% and 4% of traffic stops respectively, versus 1% for white drivers), but the searches of these drivers only yield contraband 60-70% of the time, compared to 80% of the time for white drivers.

Translation - Black drivers are 500% more likely to be searched than white drivers during a traffic stop, but are 20% less likely to be caught with contraband in the event of a search.

### 2.5 - Compare Search Stats By Race and Location

Let's add in location as another factor.  It's possible that some counties (such as those were opiod trafficing is prevalent) have a much higher search rate / lower hit rates for both white and non-white drivers, leading to distortion in the overall stats.  By controlling for location, we can determine if this is the case.

We'll define a new function to generate the visualization.
```python
def visualize_search_stats_by_county(df):
    """Generate a scatter plot of search rate vs. hit rate by race and county"""
    race_location_agg = df.groupby(['county_name','driver_race']).apply(compute_search_stats)

    fig, ax = plt.subplots()
    for c, frame in race_location_agg.groupby('driver_race'):
        ax.scatter(x=frame['hit_rate'], y=frame['search_rate'], label=c)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2),
              ncol=5, fancybox=True)
    ax.set_xlabel('Hit Rate')
    ax.set_ylabel('Search Rate')
```

Let's run our new function to generate a scatter plot.

```python
visualize_search_stats_by_county(df_vt)
```

Each dot in the above chart represents a county.  You'll notice that only one county is represented for Asian drivers - this is due to the lack of data for Asian drivers in other counties.

**In the above visualization, we can see a clear pattern of discrimination in traffic stop searches.**

The search rates and hit rates for white drivers in most counties are quite consistently clustered around 80% and 1% respectively.  We can see, however, that nearly every county searches black and hispanic drivers at a higher rate, and that these searches uniformally have a lower hit rate than those on white drivers.

This state-wide pattern of a higher search rate combined with a lower hit rate suggests that a lower standard of evidence is used when deciding to search black and hispanic drivers compared to when searching white drivers.

# 3 - Analyzing Other States

### 3.0 - Massachuesstts
Let's now perform the same analysis on my home state, Massachusetts.  This time we'll have a bit more data to work with - roughly 3.4 million traffic stops.

Download the dataset to your project's `/data` directory - https://stacks.stanford.edu/file/druid:py883nd2578/MA-clean.csv.gz

Then load the dataset (this time we'll only load the columns that we're examining, in order to save memory), and remove rows with missing data.
```python
fields = ['county_name', 'driver_race', 'search_conducted', 'contraband_found']
df_ma = pd.read_csv('./data/MA-clean.csv.gz', compression='gzip', low_memory=False, usecols=fields)
df_ma.dropna(inplace=True)
```

Let's generate a statewide table of search rate and hit rate by race.

```python
df_ma.groupby('driver_race').apply(compute_search_stats)
```

< insert table >

We can see here again that black and hispanic drivers are searched at significantly higher rates than white drivers. The differences in hit rates are not as extreme as in Vermont, but they are still noticeably lower for black and hispanic drivers than for whites.  Asian drivers, interestingly, are the least likely to be searched and also the least likely to have contraband if they are searched.

If we compare the stats for MA to VT, we'll also notice that police in MA seem to use a much lower standard of evidence when searching a vehicle, with their searches averaging around 50% hit rate, compared to 80% in VT.

Let's generate the scatter plot too, to examine the stats visually.

```python
visualize_search_stats_by_county(df_ma)
```

< insert chart >

The trend here is much less obvious than in Vermont, but it's still clear that traffic stops of minority drivers tend to be more likely to result in a search, even though the hit rates are *generally* lower than they are for white drivers.

### 3.1 - Wisconsin

Wisconsin has caught quite a bit of flack recently for being "a bad place to live if you're not white" (include news articles).

Let's see how their police stats stack up.

Again, you'll need to download the Wisconsin dataset to your project's `/data` directory - https://stacks.stanford.edu/file/druid:py883nd2578/WI-clean.csv.gz


```python
df_wi = pd.read_csv('./data/WI-clean.csv.gz', compression='gzip', low_memory=False, usecols=fields)
df_wi.dropna(inplace=True)
```

We'll again compute the search stats using our handy helper method.

```python
df_wi.groupby('driver_race').apply(compute_search_stats)
```

< insert table >

The trends here should be starting to look familiar.  White drivers in Wisconsin are much less likely to be searched than non-white drivers (aside from Asians, who tend to be searched at the same rate as whites).  Despite the much higher search rates, searches of non-white drivers are, again, actually less likely on average to yield contraband than searches on white drivers.

We'll visualize the same result, by county, in our scatterplot.

< insert chart >

Starting to look familiar?  We can see in the chart bellow that the standard of evidence for searching non-white drivers is higher in virtually every county than for white drivers.  In one outlying county, almost 25% (!) of traffic stops for black drivers resulted in a search, even though only 50% of those searches yielded contraband.

You've heard the phrase "A picture is worth a thousand words"?  This is one of those pictures - and the name of the picture is "Systemic Racism".

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