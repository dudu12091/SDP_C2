# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 15:00:15 2021

@author: Danie
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

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

#classifying all rows into sizes
df_allRepos["Size_Classification"]=np.NaN

j=0 #start of class (i is end of class)
n=3 #number of splits
classifier_number = 0 #classification for sizes
stepSize = round(len(df_allRepos)/n) # splitting into n equally sized splits

#iteratively assign size classifications to equally sized sets based on the specified n splits
for i in range(stepSize,len(df_allRepos),stepSize):
    df_allRepos["Size_Classification"][j:i]=classifier_number
    classifier_number+=1
    j=i
#for the final step go from the start to the very end
df_allRepos["Size_Classification"][j:]=classifier_number


#saving all repos with their new size classifications
df_allRepos.to_csv("./EqualSizeSplit_All.csv", index=False, header=True)

# Visualisations and useful figures for the different sizes

# Box Plot representing 1: Small, 2: Medium, 3: Large and the averages of stars
small_loc = df_allRepos.loc[df_allRepos['Size_Classification'] == 0.0]
medium_loc = df_allRepos.loc[df_allRepos['Size_Classification'] == 1.0]
large_loc = df_allRepos.loc[df_allRepos['Size_Classification'] == 2.0]
data = [small_loc['LOC'], medium_loc['LOC'], large_loc['LOC']]

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111)
ax.set_title('Boxplot showing LOC distribution between Small, Medium and Large Repositories')
ax.set_xlabel('Type of Repository')
ax.set_ylabel('LOC')
ax.set_xticklabels(['Small', 'Medium', 'Large'])
ax.get_yaxis().get_major_formatter().set_scientific(False)
bp = ax.boxplot(data)

# Box Plot showing the distribution of stars
star_data = df_allRepos['Stars']
fig_4 = plt.figure(figsize=(10,7))
ax_4 = fig_4.add_subplot(111)
ax_4.set_title('Boxplot showing Stars given to Repositories')
ax_4.set_ylabel('Stars')
star_bp = ax_4.boxplot(star_data)

plt.figtext(0.5, 0.01, f"Mean: {star_data.mean()}, Median: {star_data.median()}, Min: {star_data.min()}, Max: {star_data.max()}", ha="center", va="center", fontsize=8)

# Histogram for LOC distribution

fig_2 = plt.figure(figsize=(10,7))
ax_2 = fig_2.add_subplot(111)
ax_2.set_title('Histogram showing LOC')
ax_2.set_xlabel('LOC')
ax_2.set_ylabel('Frequency')
ax_2.get_xaxis().get_major_formatter().set_scientific(False)
hist_loc = ax_2.hist(df_allRepos['LOC'])

plt.figtext(0.5, 0.01, f"Mean: {df_allRepos['LOC'].mean()}, Median: {df_allRepos['LOC'].median()}, Min: {df_allRepos['LOC'].min()}, Max: {df_allRepos['LOC'].max()}, Mode: {df_allRepos['LOC'].mode()}", ha="center", va="center", fontsize=8)

# Histogram for Stars distribution

fig_3 = plt.figure(figsize=(10,7))
ax_3 = fig_3.add_subplot(111)
ax_3.set_title('Histogram showing Stars')
ax_3.set_xlabel('Stars')
ax_3.set_ylabel('Frequency')
ax_3.get_xaxis().get_major_formatter().set_scientific(False)
hist_loc = ax_3.hist(df_allRepos['Stars'])

plt.figtext(0.5, 0.01, f"Mean: {df_allRepos['Stars'].mean()}, Median: {df_allRepos['Stars'].median()}, Min: {df_allRepos['Stars'].min()}, Max: {df_allRepos['Stars'].max()}, Mode: {df_allRepos['Stars'].mode()}", ha="center", va="center", fontsize=8)

plt.show()

# add any other useful ones

# Line graph showing if there is a correlation between number of stars and repository size



#getting best/worst rated for each size
df_bestRepos = pd.DataFrame(columns=["Name","Repository","Stars","LOC","Size_Classification","Best_or_worst"])

n_best = 10
#n_worst = 10 
gb_allRepos = df_allRepos.groupby("Size_Classification")
for group_name, df_sizeGroup in gb_allRepos:
    df_sizeGroup=df_sizeGroup.sort_values(by="Stars")
    
    #df_nWorst = df_sizeGroup.head(n_worst)
    #df_nWorst["Best_or_worst"]="worst"
    df_nBest = df_sizeGroup.tail(n_best)
    df_nBest["Best_or_worst"]="best"
    
    #df_bestRepos=df_bestRepos.append(df_nWorst)
    df_bestRepos=df_bestRepos.append(df_nBest)

df_bestRepos.to_csv("./EqualSizeSplit_Best.csv", index=False, header=True)
    

