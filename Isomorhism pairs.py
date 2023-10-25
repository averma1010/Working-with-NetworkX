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

df = pd.read_csv('')

## Grouping the data by 3 days to get a less sparse graph and also because links don't really expire

grouped = df.groupby(pd.Grouper(key='Day', freq='3D'))

## Capturing the largest connected component in an interval
largest_connected_component = {}

## Will capture the largest connected component in the dictionay


for interval_start, group_df in grouped:
     try:
         Graph = nx.from_pandas_edgelist(group_df, 'Source', 'Target') ## Creates a networkx object called graph
     except:
         pass ## Some intervals might not have any nodes, so to this just passes over them
     try:
         Gcc = sorted(nx.connected_components(Graph), key=len, reverse=True) ## nx.connect_components find all the connected components in the network, and then we sort it through the number of nodes in the connected component
         G0 = Graph.subgraph(Gcc[0]) ## This takes the largest connected component in the network
     except:
         pass
     
     largest_connected_component[interval_start] = G0 ## Adding the largest connected component as the value, key would be the interval start date



## Will now check for isomorphisms of the largest connected components at every interval

keys = list(largest_connected_component.keys())
isomorphic_pairs = []

for i in range(len(keys)): 
    for j in range(i+1, len(keys)):
        datetime1, subgraph1 = keys[i], largest_connected_component[keys[i]]
        datetime2, subgraph2 = keys[j], largest_connected_component[keys[j]]
        if nx.is_isomorphic(subgraph1, subgraph2): ## Checking for isomorphism
            isomorphic_pairs.append((datetime1, datetime2))

print("Pairs of isomorphic subgraphs:")
print(isomorphic_pairs)
     