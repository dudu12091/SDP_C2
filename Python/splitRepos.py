import pandas as pd
import xlwt

names = pd.read_excel('ApacheRepositoryStats.xls')['Name'].values
url = pd.read_excel('ApacheRepositoryStats.xls')['Repository'].values
commits = pd.read_excel('ApacheRepositoryStats.xls')['Commits'].values
stars = pd.read_excel('ApacheRepositoryStats.xls')['Stars'].values

repos_stars = {}
for i in range(len(names)):
    if stars[i].find('k') > -1:
        star = int(float(stars[i][:stars[i].find('k')]) * 1000)
    else:
        star = int(stars[i])
    repos_stars[names[i]] = star
repos_url = {}
for i in range(len(names)):
    repos_url[names[i]] = url[i]

probability = [float(z/sum(commits)) for z in commits]
repos_p = []
for i in range(len(names)):
    repos_p.append((names[i], probability[i]))
repos_p = sorted(repos_p, key=lambda x: x[1])
small_repos = []
medium_repos = []
large_repos = []
threshold_s = float(1/3)
threshold_m = float(2/3)
p = 0.0
for i in range(len(repos_p)):
    if p < threshold_s:
        small_repos.append((repos_p[i][0], repos_stars[repos_p[i][0]]))
    elif p < threshold_m:
        medium_repos.append((repos_p[i][0], repos_stars[repos_p[i][0]]))
    else:
        large_repos.append((repos_p[i][0], repos_stars[repos_p[i][0]]))
    p += repos_p[i][1]

small_repos = sorted(small_repos, key=lambda x: x[1], reverse=True)
medium_repos = sorted(medium_repos, key=lambda x: x[1], reverse=True)
large_repos = sorted(large_repos, key=lambda x: x[1], reverse=True)

print("save.....")
book = xlwt.Workbook(encoding="utf-8", style_compression=0)
sheet = book.add_sheet('RepositorySubject', cell_overwrite_ok=True)
col = ("Name", "Repository", "Stars")
for i in range(0, 3):
    sheet.write(0, i, col[i])
for i in range(10):
    name = small_repos[i][0]
    url = repos_url[name]
    star = small_repos[i][1]
    repo = [name, url, star]
    for j in range(len(repo)):
        sheet.write(i+1, j, repo[j])
for i in range(10, 20):
    name = medium_repos[i-10][0]
    url = repos_url[name]
    star = medium_repos[i-10][1]
    repo = [name, url, star]
    for j in range(len(repo)):
        sheet.write(i+1, j, repo[j])
for i in range(20, 30):
    name = large_repos[i-20][0]
    url = repos_url[name]
    star = large_repos[i-20][1]
    repo = [name, url, star]
    for j in range(len(repo)):
        sheet.write(i+1, j, repo[j])
book.save("ApacheRepositorySplit.xls")



