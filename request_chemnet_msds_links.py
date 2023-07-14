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
    tr_tags = soup.find_all('tr', {'bgcolor': 'fffff1'})
    links = []
    for tag in tr_tags:
        elements = tag.find_all('a')
        for element in elements:
            link = element['href']
            links.append(link)
    return links


"""
从网站中获取最大页码。

参数:
- num (int): 要从中获取数据的页码。

返回值:
- int: 网站上找到的最大页码。
"""
def get_max_page_number(num):
    url = f"http://cheman.chemnet.com/notices/index.cgi?p=1&f=&t=notices&ra=&terms=&mt={num}"
    response = requests.get(url, headers=headers)
    html_code = response.text
    soup = BeautifulSoup(html_code, 'html.parser')
    tr_tags = soup.find_all('tr', {'bgcolor': 'fffff1'})
    links = tr_tags.find_all('a')
    max_page = 0
    for link in links:
        page = int(link.text)
        if page > max_page:
            max_page = page
    return max_page

# 从网站中获取所有链接  这里18是有17个笔画，按笔画遍历
for num in range(1, 18):
    print("笔画：",num)
    # 最大页数8页
    for page in range(1, 8):
        print("页码：",page)
        url = f"http://cheman.chemnet.com/notices/index.cgi?p={page}&f=&t=notices&ra=&terms=&mt={num}"
        links = get_links(url)
        for link in links:
            # 将链接逐个保存到本地文件
            file_path = "links.txt"
            with open(file_path, "a") as file:
                file.write(link + "\n")
    # 随机延迟1-3秒
    delay = random.uniform(1, 3)
    time.sleep(delay)
