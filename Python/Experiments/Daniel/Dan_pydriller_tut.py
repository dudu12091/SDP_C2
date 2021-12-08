from pydriller import Repository
import pandas as pd

from datetime import datetime

i=0 # remove this and all if statements for breaking early - just so it finishes in reasonable time

print("local repo\n")
repo = Repository(r"\Users\Danie\Documents\Uni\UCL")

for commit in repo.traverse_commits():
    print(commit.hash)
    print(commit.msg)
    # print(commit.author.name)
    # for file in commit.modified_files:
    #     print(file.filename, ' has changed')
    i+=1
    if(i%5==0):
        break
    
    
    
#example for my remote repo I own
print("\n\n\nremote repo I own\n")
#repo = Repository(r"D:\Users\Danie\Documents\Uni\UCL")
repo2 = Repository(r"https://github.com/danielmusselwhite/SDP_CW2")

for commit in repo2.traverse_commits():
    print(commit.hash)
    print(commit.msg)
    # print(commit.author.name)
    # for file in commit.modified_files:
    #     print(file.filename, ' has changed')
    i+=1
    if(i%5==0):
        break
    
    
#example for a remote repo I don't own
print("\n\n\nremote repo I don't own\n")

repo3 = Repository('https://github.com/ishepard/pydriller')
for commit in repo3.traverse_commits():
    print(commit.hash)
    print(commit.msg)
    # print(commit.author.name)
    # for file in commit.modified_files:
    #     print(file.filename, ' has changed')
    i+=1
    if(i%5==0):
        break


#example for 1 of the apache URLs
print("\n\n\none specific apache URL\n")

dt1 = datetime(2021, 12, 6, 0, 0, 0)
dt2 = datetime(2021, 12, 8, 0, 0, 0)

repo4 = Repository("https://github.com/apache/hadoop.git", since=dt1, to=dt2)

for commit in repo4.traverse_commits():
    print(commit.hash)
    print(commit.msg)
    # print(commit.author.name)
    # for file in commit.modified_files:
    #     print(file.filename, ' has changed')
    i+=1
    if(i%5==0):
        break

    
    
#example for all apache URLs
print("\n\n\nAll apache URL\n")
urls = pd.read_excel('../../ApacheRepository.xls')['Repository']

#repo = Repository(urls)

#for commit in repo.traverse_commits():
#    print("hash :", commit.hash)
