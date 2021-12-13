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




# visualisations and useful figures

#Is there a better way of doing a box plot?
pivot_allRepos = df_allRepos.pivot_table(index="Stars", columns='Size_Classification', values='LOC')
pivot_allRepos.plot(kind='box', figsize=[16,8])

#add histogram here

#add any other useful ones