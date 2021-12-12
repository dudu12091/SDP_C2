import pandas

f1 = pandas.read_excel("ApacheRepository.xls")
f2 = pandas.read_excel("RepositoryCommitsSize.xlsx")

# I manually deleted the 'manual stars rank column'
f3 = f1[["Name", "Repository", "Stars"]].merge(f2[["Name", "Commits", "Manual Stars Rank"]], on = "Name", how = "left")

f3.to_excel("ApacheRepositoryStats.xls", index = False)