from pydriller import Repository
import pandas as pd

from datetime import datetime

#example for my local repo
print("local repo\n")
repo = Repository(r"D:\Users\Danie\Documents\Uni\UCL")

for commit in repo.traverse_commits():
    print("hash :", commit.hash)

dt1 = datetime(2016, 10, 8, 17, 0, 0)
dt2 = datetime(2016, 11, 8, 17, 59, 0)


#example for 1 of the apache URLs
print("\n\n\n1 apache URL\n")
urls = pd.read_excel('../../ApacheRepository.xls')['Repository']

repo2 = Repository("https://github.com/apache/hadoop.git")

for commit in repo2.traverse_commits():
    print("hash :", commit.hash)

    
    
#example for all apache URLs
print("\n\n\nAll apache URL\n")
urls = pd.read_excel('../../ApacheRepository.xls')['Repository']

#repo = Repository(urls)

#for commit in repo.traverse_commits():
#    print("hash :", commit.hash)
