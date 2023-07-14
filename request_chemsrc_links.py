import requests
from bs4 import BeautifulSoup
import random
import time

print("开始爬取")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

"""
从指定的URL获取所有链接。
参数:
    url (str): 要从中获取链接的URL。
返回值:
    list: 包含页面上所有链接的列表。
"""
def get_links(url):
    response = requests.get(url, headers=headers)
    html_code = response.text
    soup = BeautifulSoup(html_code, 'html.parser')
    # 找到id为idxTbl的table元素
    table = soup.find('table', id='idxTbl')
    links = []
    # 遍历table中的每个a标签，并输出链接
    for a_tag in table.find_all('a'):
        # 判断a标签是否具有style属性，并且style属性值为'color:#337ab7'
        if a_tag.has_attr('style') and a_tag['style'] == 'color:#337ab7':
            link = a_tag['href']
            links.append(link)
    print(links)
    return links

# 从网站中获取所有链接
for page in range(1, 4412):
    print("页码：",page)
    url = f"https://www.chemsrc.com/casindex/{page}.html"
    links = get_links(url)
    for link in links:
        # 将链接逐个保存到本地文件
        file_path = "src_links.txt"
        with open(file_path, "a") as file:
            file.write(link + "\n")
    # 随机延迟3-6秒
    delay = random.uniform(3, 6)
    time.sleep(delay)
