import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os


# the total number of repositories
repo_num = 30
# number of repositories for each size
repo_num_each_size = 10

df = pd.read_csv('Repository_info.csv')

# if 'TDD probability' > benchmark, we consider it's a TDD repository
benchmark = 0.7

###############################################################################
####### 1. Inspect likelihood for a project to be TDD over all repos ##########
###############################################################################

# the number of TDD repositories
TDD_num = 0;
# the name of TDD repositories
TDD_repos = np.array([])
for i in range(len(df)):
    if df.iloc[i][10] > benchmark:
        TDD_num += 1
        TDD_repos = np.append(TDD_repos, df.iloc[i][1])
        
print("the number of TDD repositories is ", TDD_num)
print("they are ", TDD_repos)

likelihood = TDD_num / repo_num
print("the likelihood for a project to be TDD over all repositories is", likelihood)


###########################################################################
####### 2. Inspect likelihood for each size of project to be TDD ##########
###########################################################################

# number of TDD repositories in small size group
TDD_num_small = 0
# number of TDD repositories in medium size group
TDD_num_medium = 0
# number of TDD repositories in large size group
TDD_num_large = 0

for i in range(len(df)):
    if df.iloc[i][10] > benchmark:
        if i < 10:
            TDD_num_small += 1
        elif i < 20:
            TDD_num_medium += 1
        else:
            TDD_num_large += 1
                      
likelihood_small = TDD_num_small / repo_num_each_size
likelihood_medium = TDD_num_medium / repo_num_each_size
likelihood_large = TDD_num_large / repo_num_each_size

print("the likelihood for small project to be TDD is", likelihood_small)
print("the likelihood for medium project to be TDD is", likelihood_medium)
print("the likelihood for large project to be TDD is", likelihood_large)

# histogram
x = range(3)
likelihood_list = [likelihood_small, likelihood_medium, likelihood_large]
likelihood_index = ["small", "medium", "large"]
plt.bar(x, likelihood_list)
plt.xticks(x, likelihood_index)
plt.title("likelihood for each size of project to be TDD")
plt.xlabel("project size")
plt.ylabel("likelihood")
plt.show()

#######################################################################################
####### 3. Inspect the popularity for TDD vs non-TDD projects over all repos ##########
#######################################################################################

# x: number of  stars
# y: TDD probability
x1 = np.array([])
x2 = np.array([])
y1 = np.array([])
y2 = np.array([])
for i in range(len(df)):
    if df.iloc[i][10] > benchmark:
        x1 = np.append(x1, df.iloc[i][2])
        y1 = np.append(y1, df.iloc[i][10])
    else:
        x2 = np.append(x2, df.iloc[i][2])
        y2 = np.append(y2, df.iloc[i][10])
        
plt.scatter(x1, y1, label="TDD repository")
plt.scatter(x2, y2, label="non-TDD repository")
plt.legend()
plt.xlabel("number of stars")
plt.ylabel("TDD probability")
plt.title("the relationship between stars and TDD probability")
plt.show()

###############################################################################################
####### 4. Inspect the popularity for TDD vs non-TDD projects for each sized project ##########
###############################################################################################

# for small projects
# x: number of  stars
# y: TDD probability
x1 = np.array([])
x2 = np.array([])
y1 = np.array([])
y2 = np.array([])
for i in range(0,10):
    if df.iloc[i][10] > benchmark:
        x1 = np.append(x1, df.iloc[i][2])
        y1 = np.append(y1, df.iloc[i][10])
    else:
        x2 = np.append(x2, df.iloc[i][2])
        y2 = np.append(y2, df.iloc[i][10])
        
plt.scatter(x1, y1, label="TDD repository")
plt.scatter(x2, y2, label="non-TDD repository")
plt.legend()
plt.xlabel("number of stars")
plt.ylabel("TDD probability")
plt.title("the relationship between stars and TDD probability in small projects")
plt.show()

# for medium projects
x1 = np.array([])
x2 = np.array([])
y1 = np.array([])
y2 = np.array([])
for i in range(10,20):
    if df.iloc[i][10] > benchmark:
        x1 = np.append(x1, df.iloc[i][2])
        y1 = np.append(y1, df.iloc[i][10])
    else:
        x2 = np.append(x2, df.iloc[i][2])
        y2 = np.append(y2, df.iloc[i][10])
        
plt.scatter(x1, y1, label="TDD repository")
plt.scatter(x2, y2, label="non-TDD repository")
plt.legend()
plt.xlabel("number of stars")
plt.ylabel("TDD probability")
plt.title("the relationship between stars and TDD probability in medium projects")
plt.show()

# for large projects
x1 = np.array([])
x2 = np.array([])
y1 = np.array([])
y2 = np.array([])
for i in range(20,30):
    if df.iloc[i][10] > benchmark:
        x1 = np.append(x1, df.iloc[i][2])
        y1 = np.append(y1, df.iloc[i][10])
    else:
        x2 = np.append(x2, df.iloc[i][2])
        y2 = np.append(y2, df.iloc[i][10])
        
plt.scatter(x1, y1, label="TDD repository")
plt.scatter(x2, y2, label="non-TDD repository")
plt.legend()
plt.xlabel("number of stars")
plt.ylabel("TDD probability")
plt.title("the relationship between stars and TDD probability in small projects")
plt.show()

###########################################################################################
####### 5. How TDD impacts the commit size and the number of bug-fixing commits? ##########
###########################################################################################

# x: name of repository
# y: average modified lines in each commit
x1 = np.array([])
x2 = np.array([])
y1 = np.array([])
y2 = np.array([])
for i in range(len(df)):
    if df.iloc[i][10] > benchmark:
        x1 = np.append(x1, df.iloc[i][1])
        y1 = np.append(y1, df.iloc[i][7]/df.iloc[i][5])
    else:
        x2 = np.append(x2, df.iloc[i][1])
        y2 = np.append(y2, df.iloc[i][7]/df.iloc[i][5])
        
# for TDD repository
x = range(len(x1))
plt.bar(x, y1)
plt.xticks(x, x1)
plt.title("the number of average modified lines in TDD repository")
plt.xlabel("name of repository")
plt.ylabel("number of average modified lines")
plt.show()

# for non-TDD repository
x = range(len(x2))
plt.bar(x, y2)
plt.xticks(x, x2)
plt.xticks(rotation=90)
plt.title("the number of average modified lines in non-TDD repository")
plt.xlabel("name of repository")
plt.ylabel("number of average modified lines")
plt.show()

# x: name of repository
# y: persentage of bug-fixing commit
x1 = np.array([])
x2 = np.array([])
y1 = np.array([])
y2 = np.array([])
for i in range(len(df)):
    if df.iloc[i][10] > benchmark:
        x1 = np.append(x1, df.iloc[i][1])
        y1 = np.append(y1, df.iloc[i][6]/df.iloc[i][5])
    else:
        x2 = np.append(x2, df.iloc[i][1])
        y2 = np.append(y2, df.iloc[i][6]/df.iloc[i][5])
        
# for TDD repository
x = range(len(x1))
plt.bar(x, y1)
plt.xticks(x, x1)
plt.title("the persentage of bug-fixing commit in TDD repository")
plt.xlabel("name of repository")
plt.ylabel("persentage of bug-fixing commit")
plt.show()

# for non-TDD repository
x = range(len(x2))
plt.bar(x, y2)
plt.xticks(x, x2)
plt.xticks(rotation=90)
plt.title("the persentage of bug-fixing commit in non-TDD repository")
plt.xlabel("name of repository")
plt.ylabel("persentage of bug-fixing commit")
plt.show()

