"""
Created on Thu Dec 20 10:20:00 2021

@author: Muna

For more info: analyticsvidhya.com/blog/2019/05/beginners-guide-hierachical-clustering/
"""

from os import link
from numpy.linalg.linalg import norm
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
df_allRepos = df_allRepos.sort_values(by=["LOC"]).reset_index()

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

# Create Dataframe for Starstried 
df_stars = df_allRepos[['ID','Stars']]

# normalise values for loc because some are very large
from sklearn.preprocessing import normalize
df_stars_scaled = normalize(df_stars)
df_stars_scaled = pd.DataFrame(df_stars_scaled, columns=df_stars.columns)

# Draw Dendrogram to help us select the number of clusters we want

"""
y axis shows the distance between the stars when we merge two repositories together
We want a threshold to get the number of clusters and how they should be divided,
we draw a horizontal line between the highest vertical line. We then have clsuters split from the left of midpoint of line and right.
"""

import scipy.cluster.hierarchy as shc
plt.figure(figsize=(10,7))
plt.title("Stars Dendrogram")
dend = shc.dendrogram(shc.linkage(df_stars_scaled, method="ward"))
plt.axhline(y=4, color='r', linestyle='--')

from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
segmentation = cluster.fit_predict(df_stars_scaled)

# Apply the split and save to Excel
for i in range(df_allRepos.shape[0]):
    df_allRepos.loc[i,'Stars_Group'] = segmentation[i]

df_allRepos.to_csv("./HierarchicalSplit_Stars.csv", index=False, header=True)

# Boxplot for Stars
size_classes = np.sort(df_allRepos["Stars_Group"].unique())
data = []
for key in df_allRepos['Stars_Group'].unique():
    data+=[df_allRepos.loc[df_allRepos['Stars_Group'] == key]["Stars"]]

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
ax.set_title('Boxplot showing Stars distribution between clustered size repos')
ax.set_xlabel('Repository size classification')
ax.set_xticklabels(size_classes)
ax.set_ylabel('Stars')
ax.get_yaxis().get_major_formatter().set_scientific(False)
bp = ax.boxplot(data)

# Bar Chart representing the distribution of size classifications: Stars
distribution_data = []
for key in df_allRepos["Stars_Group"].unique():
    distribution_data+=[len(df_allRepos.loc[df_allRepos['Stars_Group'] == key]["Stars"])]
    
fig_2 = plt.figure(figsize=(10,7))
ax_2 = fig_2.add_subplot(111)
ax_2.set_title('Stars - Barchart showing distribution between different size classifications')
ax_2.set_xlabel('Size classification of Repository')
ax_2.set_ylabel('Number of repositories classified as this')
ax_2.get_yaxis().get_major_formatter().set_scientific(False)

x_pos = [i for i, _ in enumerate(size_classes)]
bp = ax_2.bar(x_pos, distribution_data)
plt.xticks(x_pos,size_classes)

"""

Hierarchical Clustering

LOC Split

"""

df_loc = df_allRepos[['ID','LOC']]

# normalise values for loc because some are very large
from sklearn.preprocessing import normalize
df_loc_scaled = normalize(df_loc)
df_loc_scaled = pd.DataFrame(df_loc_scaled, columns=df_loc.columns)

import scipy.cluster.hierarchy as shc
plt.figure(figsize=(10,7))
plt.title("LOC Dendrogram")
dend = shc.dendrogram(shc.linkage(df_loc_scaled, method="ward"))
plt.axhline(y=0.4, color='r', linestyle='--')

from sklearn.cluster import AgglomerativeClustering
cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
segmentation = cluster.fit_predict(df_loc_scaled)

# Apply the split and save to Excel
for i in range(df_allRepos.shape[0]):
    df_allRepos.loc[i,'LOC_Group'] = segmentation[i]

df_allRepos.to_csv("./HierarchicalSplit_LOC.csv", index=False, header=True)


# Boxplot for LOC
size_classes = np.sort(df_allRepos["LOC_Group"].unique())
data = []
for key in df_allRepos['LOC_Group'].unique():
    data+=[df_allRepos.loc[df_allRepos['LOC_Group'] == key]["LOC"]]

fig_1 = plt.figure(figsize=(10,7))
ax_1 = fig_1.add_subplot(111)
ax_1.set_title('Boxplot showing LOC distribution between clustered size repos')
ax_1.set_xlabel('Repository size classification')
ax_1.set_xticklabels(size_classes)
ax_1.set_ylabel('LOC')
ax_1.get_yaxis().get_major_formatter().set_scientific(False)
bp = ax_1.boxplot(data)

# Bar Chart representing the distribution of size classifications: LOC
distribution_data = []
for key in df_allRepos["LOC_Group"].unique():
    distribution_data+=[len(df_allRepos.loc[df_allRepos['LOC_Group'] == key]["LOC"])]
    
fig_3 = plt.figure(figsize=(10,7))
ax_3 = fig_3.add_subplot(111)
ax_3.set_title('LOC - Barchart showing distribution between different size classifications.')
ax_3.set_xlabel('Size classification of Repository')
ax_3.set_ylabel('Number of repositories classified as this')
ax_3.get_yaxis().get_major_formatter().set_scientific(False)

x_pos = [i for i, _ in enumerate(size_classes)]
bp = ax_3.bar(x_pos, distribution_data)
plt.xticks(x_pos,size_classes)

plt.show()
