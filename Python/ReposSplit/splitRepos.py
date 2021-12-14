import pandas as pd
import xlwt
import matplotlib.pyplot as plt

names = pd.read_excel('ApacheReposInfo2.xlsx')['Name'].values
url = pd.read_excel('ApacheReposInfo2.xlsx')['Repository'].values
loc = pd.read_excel('ApacheReposInfo2.xlsx')['LOC'].values
stars = pd.read_excel('ApacheReposInfo2.xlsx')['Stars'].values

repos_stars = {}
for i in range(len(names)):
    stars[i] = str(stars[i])
    if stars[i].find('k') > -1:
        star = int(float(stars[i][:stars[i].find('k')]) * 1000)
    else:
        star = int(stars[i])
    repos_stars[names[i]] = star
repos_url = {}
for i in range(len(names)):
    repos_url[names[i]] = url[i]

repos_line = {}
for i in range(len(loc)):
    temp = str(loc[i])
    if temp.find('k') > -1:
        line = int(float(temp[:temp.find('k')]))*1000
    elif temp.find('m') > -1:
        line = int(float(temp[:temp.find('m')])) * 1000000
    else:
        line = int(temp)
    repos_line[names[i]] = line
repos_line_list = sorted(repos_line.items(), key=lambda kv: (kv[1], kv[0]))

small_repos = []
medium_repos = []
large_repos = []
threshold_s = len(names) / 3
threshold_m = 2*len(names) / 3
p = 0
for i in range(len(repos_line_list)):
    if p < threshold_s:
        small_repos.append((repos_line_list[i][0], repos_stars[repos_line_list[i][0]], repos_line_list[i][1]))
    elif p < threshold_m:
        medium_repos.append((repos_line_list[i][0], repos_stars[repos_line_list[i][0]], repos_line_list[i][1]))
    else:
        large_repos.append((repos_line_list[i][0], repos_stars[repos_line_list[i][0]], repos_line_list[i][1]))
    p += 1

small_repos = sorted(small_repos, key=lambda x: x[1], reverse=True)
medium_repos = sorted(medium_repos, key=lambda x: x[1], reverse=True)
large_repos = sorted(large_repos, key=lambda x: x[1], reverse=True)

print("save.....")
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('RepositoryBestSubject', cell_overwrite_ok=True)
col = ("Name", "Repository", "Stars", "LOC")
for i in range(0, 4):
    sheet.write(0, i, col[i])
for i in range(10):
    name = small_repos[i][0]
    url = repos_url[name]
    star = small_repos[i][1]
    line = small_repos[i][2]
    repo = [name, url, star, line]
    for j in range(len(repo)):
        sheet.write(i+1, j, repo[j])
for i in range(10, 20):
    name = medium_repos[i-10][0]
    url = repos_url[name]
    star = medium_repos[i-10][1]
    line = medium_repos[i-10][2]
    repo = [name, url, star, line]
    for j in range(len(repo)):
        sheet.write(i+1, j, repo[j])
for i in range(20, 30):
    name = large_repos[i-20][0]
    url = repos_url[name]
    star = large_repos[i-20][1]
    line = large_repos[i-20][2]
    repo = [name, url, star, line]
    for j in range(len(repo)):
        sheet.write(i+1, j, repo[j])
small_repos = sorted(small_repos, key=lambda x: x[1], reverse=False)
medium_repos = sorted(medium_repos, key=lambda x: x[1], reverse=False)
large_repos = sorted(large_repos, key=lambda x: x[1], reverse=False)
sheet2 = book.add_sheet('RepositoryWorstSubject', cell_overwrite_ok=True)
for i in range(0, 4):
    sheet2.write(0, i, col[i])
for i in range(10):
    name = small_repos[i][0]
    url = repos_url[name]
    star = small_repos[i][1]
    line = small_repos[i][2]
    repo = [name, url, star, line]
    for j in range(len(repo)):
        sheet2.write(i+1, j, repo[j])
for i in range(10, 20):
    name = medium_repos[i-10][0]
    url = repos_url[name]
    star = medium_repos[i-10][1]
    line = medium_repos[i-10][2]
    repo = [name, url, star, line]
    for j in range(len(repo)):
        sheet2.write(i+1, j, repo[j])
for i in range(20, 30):
    name = large_repos[i-20][0]
    url = repos_url[name]
    star = large_repos[i-20][1]
    line = large_repos[i-20][2]
    repo = [name, url, star, line]
    for j in range(len(repo)):
        sheet2.write(i+1, j, repo[j])
book.save("ApacheRepositorySplit2.xls")



