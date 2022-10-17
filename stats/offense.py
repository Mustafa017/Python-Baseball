import pandas as pd
import matplotlib.pyplot as plt
from data import games

plays = games[games['type'] == 'play']

plays.columns = ['type', 'inning', 'team', 'player',
                 'count', 'pitches', 'event', 'game_id', 'year']

# Select Only Hits
# The question we want to answer in this plot is: "What is the distribution of hits across innings?"
hits = plays.loc[plays['event'].str.contains(
    '^(?:S(?!B)|D|T|HR)'), ['inning', 'event']]

# Convert Column Type
hits.loc[:, 'inning'] = pd.to_numeric(hits.loc[:, 'inning'])

# Replace Dictionary
# The event column of the hits DataFrame now contains event information of various configurations.
# It contains where the ball was hit and other information that isn't needed. We will replace this
# with the type of hit for grouping later on.

# Create a dictionary called replacements that contains the following key value pairs

replacements = {r'^S(.*)': 'single',
                r'^D(.*)': 'double',
                r'^T(.*)': 'triple',
                r'^HR(.*)': 'hr'}

# Replace Function
hit_type = hits['event'].replace(replacements, regex=True)

# Add A New Column
hits = hits.assign(hit_type=hit_type)

# Group By Inning and Hit Type
hits = hits.groupby(['inning', 'hit_type']).size().reset_index(name='count')

# Convert Hit Type to Categorical
# Pass a second parameter as a list 'single', 'double', 'triple', and 'hr'. This specifies the order.
hits['hit_type'] = pd.Categorical(
    hits['hit_type'], ['single', 'double', 'triple', 'hr'])

# Sort Values
hits = hits.sort_values(['inning', 'hit_type'])

# Reshape With Pivot
# We need to reshape the hits DataFrame for plotting.
hits = hits.pivot(index='inning', columns='hit_type', values='count')

# Stacked Bar Plot
hits.plot.bar(stacked=True)
plt.show()

# print(hits.head())
