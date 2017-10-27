
# coding: utf-8

# # Project Setup

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[2]:


figsize = (16,8)


# # Dataset Exploration

# ## Load Dataset

# In[3]:


df_vt = pd.read_csv('./data/VT-clean.csv.gz', compression='gzip', low_memory=False)


# In[4]:


df_vt.head()


# In[5]:


df_vt.columns


# ## Clean Dataset

# In[6]:


df_vt.count()


# In[7]:


# Fill missing search type values with placeholder
df_vt['search_type'].fillna('N/A', inplace=True)

# Drop rows with missing values
df_vt.dropna(inplace=True)


# In[8]:


df_vt.count()


# ## Explore Data

# In[9]:


df_vt['county_name'].value_counts()


# In[10]:


df_vt['violation_raw'].value_counts()


# In[11]:


df_vt['violation'].value_counts()


# In[12]:


df_vt['stop_outcome'].value_counts()


# In[13]:


df_vt['driver_gender'].value_counts()


# In[14]:


df_vt['driver_race'].value_counts()


# In[15]:


df_vt = df_vt[df_vt['driver_race'] != 'Other']


# In[16]:


fig, ax = plt.subplots(figsize=(20,8))
ax.set_xlim(15, 70)
for race in df_vt['driver_race'].unique():
    s = df_vt[df_vt['driver_race'] == race]['driver_age']
    s.plot.kde(ax=ax, label=race)
ax.legend()

fig.savefig('images/race_age_dist.png', bbox_inches='tight')


# # Analyze Violation and Outcome Data

# In[17]:


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


# In[18]:


compute_outcome_stats(df_vt)


# In[19]:


df_vt.groupby('driver_gender').apply(compute_outcome_stats)


# In[20]:


df_vt.groupby('driver_race').apply(compute_outcome_stats)


# In[21]:


race_agg = df_vt.groupby(['driver_race']).apply(compute_outcome_stats)
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=figsize)
race_agg['citations_per_warning'].plot.barh(ax=axes[0], figsize=figsize, title="Citation Rate By Race")
race_agg['arrest_rate'].plot.barh(ax=axes[1], figsize=figsize, title='Arrest Rate By Race')

fig.savefig('images/citations_and_arrests_by_race.png', bbox_inches='tight')


# In[22]:


df_vt.groupby(['driver_race','violation']).apply(compute_outcome_stats)


# In[23]:


# Create new column to represent whether the driver is White
df_vt['is_white'] = df_vt['driver_race'] == 'White'

# Remove violation with too few data points
df_vt_filtered = df_vt[~df_vt['violation'].isin(['Other (non-mapped)', 'DUI'])]


# In[24]:


df_vt_filtered.groupby(['is_white','violation']).apply(compute_outcome_stats)


# In[25]:


df_vt_filtered = df_vt[~df_vt['violation'].isin(['Other (non-mapped)', 'DUI'])]


# In[26]:


race_stats = df_vt_filtered.groupby(['violation', 'driver_race']).apply(compute_outcome_stats).unstack()
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
race_stats.plot.bar(y='arrest_rate', ax=axes[0], title='Arrest Rate By Race and Violation')
race_stats.plot.bar(y='citations_per_warning', ax=axes[1], title='Citations Per Warning By Race and Violation')
                                                       
fig.savefig('images/citations_and_arrests_by_race_and_violation.png', bbox_inches='tight')


# In[27]:


gender_stats = df_vt_filtered.groupby(['violation','driver_gender']).apply(compute_outcome_stats).unstack()
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
ax_gender_arrests = gender_stats.plot.bar(y='arrest_rate', ax=axes[0], title='Arrests By Gender and Violation', figsize=figsize)
ax_gender_citations = gender_stats.plot.bar(y='citations_per_warning', ax=axes[1], title='Citations By Gender and Violation', figsize=figsize)

fig.savefig('images/citations_and_arrests_by_gender_and_violation.png', bbox_inches='tight')


# # Analyze Search Data

# In[28]:


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


# In[29]:


compute_search_stats(df_vt)


# In[30]:


df_vt.groupby('driver_gender').apply(compute_search_stats)


# In[31]:


age_groups = pd.cut(df_vt["driver_age"], np.arange(15, 70, 5))
df_vt.groupby(age_groups).apply(compute_search_stats)


# In[32]:


df_vt.groupby('driver_race').apply(compute_search_stats)


# In[33]:


def generate_comparison_scatter(df, ax, state, race, field, color):
    """Generate scatter plot comparing field for white drivers with minority drivers"""
    race_location_agg = df.groupby(['county_fips','driver_race']).apply(compute_search_stats).reset_index().dropna()    
    race_location_agg = race_location_agg.pivot(index='county_fips', columns='driver_race', values=field)
    ax = race_location_agg.plot.scatter(ax=ax, x='White', y=race, s=150, label=race, color=color)
    return ax


# In[34]:


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


# In[35]:


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


# In[36]:


fig = generate_comparison_scatters(df_vt, 'VT')
fig.savefig('images/search_scatters_VT.png', bbox_inches='tight')


# In[37]:


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


# In[38]:


fig = generate_county_search_stats_scatter(df_vt, "VT")
fig.savefig('images/county_scatter_VT.png', bbox_inches='tight')


# # Other States

# In[39]:


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
    
    search_scatters = generate_comparison_scatters(df, state)
    search_scatters.savefig('images/search_scatters_{}.png'.format(state), bbox_inches='tight')

    county_scatter = generate_county_search_stats_scatter(df, state)
    county_scatter.savefig('images/county_scatter_{}.png'.format(state), bbox_inches='tight')
    
    return df.groupby('driver_race').apply(compute_search_stats)


# In[40]:


#analyze_state_data('VT')


# In[41]:


analyze_state_data('MA')


# In[42]:


analyze_state_data('WI')


# In[43]:


analyze_state_data('CT')


# In[44]:


analyze_state_data('AZ')


# In[45]:


analyze_state_data('CO')


# In[46]:


analyze_state_data('NC')


# In[47]:


analyze_state_data('WA')


# In[48]:


analyze_state_data('TX')

