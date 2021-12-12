import urllib.error
import urllib.request
import re
from bs4 import *
from requests.models import Response
import xlwt
import ssl
import requests


context = ssl._create_unverified_context()
link = re.compile(r'href="(.*?)"')
repo_license = re.compile(r'Apache-2.0')


def get_data(base_url):
    data_list = []
    for i in range(1, 35):
        url = base_url + str(i)
        html = ask_url(url)

        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all('li', class_="Box-row"):
            item = str(item)
            # print(item)
            item_license = re.findall(repo_license, item)
            if len(item_license) > 0:
                link_url = re.findall(link, item)[0]
                repo_name = link_url[8:]
                link_url = "https://github.com"+link_url+".git"
                stars_count = getStars(link_url)
                #print(link_url)
                print(repo_name)
                print(stars_count)
                data_list.append([repo_name, link_url, stars_count])
    #print(len(data_list))
    return data_list


def ask_url(url):
    head = {
        "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request, context=context)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def save_data(data_list, save_path):
    print("save.....")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)
    sheet = book.add_sheet('ApacheJavaRepository', cell_overwrite_ok=True)
    col = ("Name", "Repository", "Stars")
    for i in range(0, 3):
        sheet.write(0, i, col[i])
    for i in range(len(data_list)):
        data = data_list[i]
        for j in range(0, 3):
            sheet.write(i+1, j, data[j])
    book.save(save_path)

def getStars(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    stars_class = "social-count js-social-count"
    stars = soup.find('a', class_=stars_class).text.strip()
    return stars

if __name__ == '__main__':
    base_url = 'https://github.com/orgs/apache/repositories?language=java&page='
    data_list = get_data(base_url)
    save_path = "ApacheRepository.xls"
    save_data(data_list, save_path)


