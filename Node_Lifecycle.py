###

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample
import datetime
import seaborn as sns

import networkx as nx
import copy
import random
import getpass
import psycopg2 as ps
import os
import re

###

# Connecting to database
df = pd.read_csv()


## The Source Name and Target Name will also serve as unique identifiers

node_lifecycles = {}

## Grouping by 3 days

grouped = df.groupby(pd.Grouper(key='Day', freq='3D'))




## The plan is to find the max number of consecutive days a node was in the largest cluster

for interval_start, group_df in grouped:
    interval_end = interval_start + pd.DateOffset(days=3)

    try:
        Graph = nx.from_pandas_edgelist(group_df, 'Source', 'Target')  # Creating Graph for each interval
    except:
        pass # Somedays the dimensions of the two columns don't match, so passing those
    try:
        largest_cluster_nodes = max(nx.connected_components(Graph), key=len)  # finding the largest connected component    
    except:
        pass # In case there is no connected components
     
    for node in largest_cluster_nodes:
            if node not in node_lifecycles:
                node_lifecycles[node] = {'current_streak': 1, 'max_streak': 1, 'end_date': interval_end}
            
                
    for node in node_lifecycles:
        if node in largest_cluster_nodes:
            

            node_lifecycles[node]['current_streak'] += 1
                
            if node_lifecycles[node]['current_streak'] > node_lifecycles[node]['max_streak']:
                node_lifecycles[node]['max_streak'] = max(node_lifecycles[node]['max_streak'], node_lifecycles[node]['current_streak'])
                node_lifecycles[node]['end_date'] = interval_end

        if node not in largest_cluster_nodes:
            node_lifecycles[node]['current_streak'] = 0

node_lifecycles_df = pd.DataFrame.from_dict(node_lifecycles, orient='index')

## Sorting the df by descending order of max streak
node_lifecycles_df = node_lifecycles_df.sort_values(by=['max_streak'],ascending = False)



## Ploting the winning streak 



streaks = node_lifecycles_df['max_streak']

plt.hist(streaks, bins=50, density=False, log=True)
plt.xlabel('Highest continous Streak Length')
plt.ylabel('Frequency (log scale)')
plt.title('Distribution of Winning Streaks')
plt.show()
        

