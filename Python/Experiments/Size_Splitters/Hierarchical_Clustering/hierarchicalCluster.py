"""
Created on Thu Dec 20 10:20:00 2021

@author: Muna

For more info: analyticsvidhya.com/blog/2019/05/beginners-guide-hierachical-clustering/
"""

from os import link
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster

"""
Data Pre-processing
"""

reject_outliers=False # are we using outliers in this?

# loading the spreadsheet containing all project sizes
df_allRepos = pd.read_excel('../ApacheReposInfo2.xlsx')

#using regex to remove 'k' and 'm' and getting the acutal number
df_allRepos["LOC"] = df_allRepos["LOC"].replace({r'[kK ]': '*1000', r'[mM ]': '*1000000'}, regex=True).map(pd.eval).astype(int) 
df_allRepos["Stars"] = df_allRepos["Stars"].replace({r'[kK ]': '*1000', r'[mM ]': '*1000000'}, regex=True).map(pd.eval).astype(int)

#sorting in size order
df_allRepos = df_allRepos.sort_values(by=["LOC"])

#outliers are messing with results: getting rid of repos which are much higher than others
if(reject_outliers):
    df_mask=df_allRepos['LOC']<=2000000
    df_allRepos = df_allRepos[df_mask]

# Add index to column in dataframe

df_allRepos.insert(0, 'ID', range(1, len(df_allRepos) + 1))

"""

Hierarchical Clustering

Stars Split

"""

# Create Dataframe for Stars
df_stars = df_allRepos[['ID','Stars']]

# Draw Dendrogram to help us select the number of clusters we want

"""
y axis shows the distance between the stars when we merge two repositories together
We want a threshold to get the number of clusters and how they should be divided,
we draw a horizontal line between the highest vertical line. We then have clsuters split from the left of midpoint of line and right.
"""

import scipy.cluster.hierarchy as shc
plt.figure(figsize=(10,7))
plt.title("Stars Dendrogram")
dend = shc.dendrogram(shc.linkage(df_stars, method="ward"))
plt.axhline(y=35000, color='r', linestyle='--')

from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
segmentation = cluster.fit_predict(df_stars)

# Apply the split and save to Excel
for i in range(df_allRepos.shape[0]):
    df_allRepos.loc[i,'Stars_Group'] = segmentation[i]

df_allRepos.to_csv("./HierarchicalSplit_Stars.csv", index=False, header=True)

"""

Hierarchical Clustering

LOC Split

"""

df_loc = df_allRepos[['ID','LOC']]

import scipy.cluster.hierarchy as shc
plt.figure(figsize=(10,7))
plt.title("LOC Dendrogram")
dend = shc.dendrogram(shc.linkage(df_loc, method="ward"))
plt.axhline(y=22000000, color='r', linestyle='--')

from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
segmentation = cluster.fit_predict(df_loc)

# Apply the split and save to Excel
for i in range(df_allRepos.shape[0]):
    df_allRepos.loc[i,'LOC_Group'] = segmentation[i]

df_allRepos.to_csv("./HierarchicalSplit_LOC.csv", index=False, header=True)

plt.show()
