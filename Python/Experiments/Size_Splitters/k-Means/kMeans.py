# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 15:31:07 2021

@author: Danie
"""

from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

reject_outliers=True # are we not using outliers in this?

# loading the spreadsheet containing all project sizes
df_allRepos = pd.read_excel('../ApacheReposInfo2.xlsx')

#using regex to remove 'k' and 'm' and getting the acutal number
df_allRepos["LOC"] = df_allRepos["LOC"].replace({r'[kK ]': '*1000', r'[mM ]': '*1000000'}, regex=True).map(pd.eval).astype(int) 
df_allRepos["Stars"] = df_allRepos["Stars"].replace({r'[kK ]': '*1000', r'[mM ]': '*1000000'}, regex=True).map(pd.eval).astype(int)
"""
# IF IT STOPS WORKING USE THIS TO FIND WHICH LINE HAS THE BUG (USED THIS TO DISCOVER ERROR IN LINE 482 WHERE THERE WAS AN 'l' CAUSING EVAL NOT TO WORK)
j=0
for i in range(99,len(df_allRepos),1):
    print(j,i)
    print(pd.eval(df_allRepos["LOC"][j:i].map(pd.eval)))
    print()
    
    #df_allRepos["LOC"][j:i] =pd.eval(df_allRepos["LOC"][j:i].map(pd.eval))
    #df_allRepos["Stars"][j:i] =pd.eval(df_allRepos["Stars"][j:i].map(pd.eval))
    
    
    j=i
"""



#sorting in size order
df_allRepos = df_allRepos.sort_values(by=["LOC"])

#outliers are messing with results: getting rid of repos which are much higher than others
if(reject_outliers):
    df_mask=df_allRepos['LOC']<=2000000
    df_allRepos = df_allRepos[df_mask]

#classifying all rows into sizes
kmeans=KMeans(n_clusters=3)
df_allRepos["Size_Classification"]= kmeans.fit_predict(df_allRepos[['LOC']])

#saving all repos with their new size classifications
df_allRepos.to_csv("./KMeansSplit_All.csv", index=False, header=True)







# Visualisations and useful figures for the different sizes

# Box Plot representing the LOC for different size classifications (generic as we want to experiment with different numbers of classes)
size_classes = np.sort(df_allRepos["Size_Classification"].unique())
data = []
for key in df_allRepos["Size_Classification"].unique():
    data+=[df_allRepos.loc[df_allRepos['Size_Classification'] == key]["LOC"]]

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
ax.set_title('Boxplot showing LOC distribution between different sized repos')
ax.set_xlabel('Repository size classification')
ax.set_xticklabels(size_classes)
ax.set_ylabel('LOC')
ax.get_yaxis().get_major_formatter().set_scientific(False)
bp = ax.boxplot(data)






# Box Plot showing the distribution of stars
star_data = []
for key in df_allRepos["Size_Classification"].unique():
    star_data+=[df_allRepos.loc[df_allRepos['Size_Classification'] == key]["Stars"]]

fig_4 = plt.figure(figsize=(10,7))
ax_4 = fig_4.add_subplot(111)
ax_4.set_xlabel('Repository size classification')
ax_4.set_xticklabels(size_classes)
ax_4.set_title('Boxplot showing Stars given to diifferent sized repos')
ax_4.set_ylabel('Stars')
star_bp = ax_4.boxplot(star_data)




# Bar Chart representing the distribution of size classifications
distribution_data = []
for key in df_allRepos["Size_Classification"].unique():
    distribution_data+=[len(df_allRepos.loc[df_allRepos['Size_Classification'] == key]["LOC"])]
    


fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
ax.set_title('Barchart showing distribution between different size classifications')
ax.set_xlabel('Size classification of Repository')
ax.set_ylabel('Number of repositories classified as this')
ax.get_yaxis().get_major_formatter().set_scientific(False)

x_pos = [i for i, _ in enumerate(size_classes)]
bp = ax.bar(x_pos, distribution_data)
plt.xticks(x_pos,size_classes)





#getting best/worst rated for each size
df_bestRepos = pd.DataFrame(columns=["Name","Repository","Stars","LOC","Size_Classification"])#,"Best_or_worst"])

n_best = 10
#n_worst = 10 
gb_allRepos = df_allRepos.groupby("Size_Classification")
for group_name, df_sizeGroup in gb_allRepos:
    df_sizeGroup=df_sizeGroup.sort_values(by="Stars")
    
    #df_nWorst = df_sizeGroup.head(n_worst)
    #df_nWorst["Best_or_worst"]="worst"
    df_nBest = df_sizeGroup.tail(n_best)
    #df_nBest["Best_or_worst"]="best"
    
    #df_bestRepos=df_bestRepos.append(df_nWorst)
    df_bestRepos=df_bestRepos.append(df_nBest)

df_bestRepos.to_csv("./kMeansSplit_Best.csv", index=False, header=True)






# removing the most popular repos from all_repos as we don't want duplicates in our control set
df_allButMostPopularRepos = pd.concat([df_allRepos, df_bestRepos, df_bestRepos]).drop_duplicates(keep=False)

# picking 10 random repos from each size classification
n_random = 10

df_random_repos = pd.DataFrame(columns=["Name","Repository","Stars","LOC","Size_Classification"])
gb_allRepos = df_allButMostPopularRepos.groupby("Size_Classification")
for group_name, df_sizeGroup in gb_allRepos:
    df_random_subset=df_sizeGroup.sample(n_random)
    df_random_repos=df_random_repos.append(df_random_subset)

df_random_repos.to_csv("./kMeansSplit_Control.csv", index=False, header=True)
















