from pydriller import Repository
import pandas as pd

urls = pd.read_excel('../../ApacheRepository.xls')['Repository']

j=0 #TODO: REMOVE THIS LIMITING NUMBER OF REPOS SO IT RUNS IN A REASONABLE TIME

#for each repo using the Apache license...
for repo_url in urls:
    print("Mining from:", repo_url)
    
    repo = Repository(repo_url) #TODO: which constaints should we add, if any? Dates? X amount of recent commits? All commits? Etc.
    
    
    i=0 #TODO: REMOVE THIS LIMITING NUMBER OF COMMITS SO IT RUNS IN A REASONABLE TIME
    
    #for each commit in this repo
    for commit in repo.traverse_commits():
        #TODO: modify from print to story in a DF which can be converted to .csv
        #TODO: decide which metadata we want; currently just hash, msg and files changed for each commit
        print(commit.hash)
        print(commit.msg)

        #print each file modified by this commit 
        for file in commit.modified_files:
          print(file.filename, ' has changed')
        print("\n")
          
        #TODO: REMOVE THIS LIMITING NUMBER OF COMMITS SO IT RUNS IN A REASONABLE TIME
        i+=1
        if(i>2):
            break
        
    #TODO: REMOVE THIS LIMITING NUMBER OF REPOS SO IT RUNS IN A REASONABLE TIME
    j+=1
    if(j>5):
        break