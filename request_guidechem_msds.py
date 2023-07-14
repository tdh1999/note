import requests
from bs4 import BeautifulSoup
import chardet
import pandas as pd

"""
从指定的URL获取所有链接。
参数:
    url (str): 要从中获取链接的URL。
返回值:
    list: 包含页面上所有链接的列表。
"""
def get_links(url):
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [element['href'] for element in soup.find_all('a', style='color:#0337cb; text-decoration:underline')]
    return links

"""
从网站中获取最大页码。

参数:
- num (int): 要从中获取数据的页码。

返回值:
- int: 网站上找到的最大页码。
"""
def get_max_page_number(num):
    url = f"https://china.guidechem.com/datacenter/msds_cn_list-{num}-p1.html"
    response = requests.get(url, headers=headers)
    html_code = response.text
    soup = BeautifulSoup(html_code, 'html.parser')
    td_element = soup.find('td', class_='digg')
    page_links = td_element.find_all('a')
    page_numbers = [link.get_text() for link in page_links]
    filtered_page_numbers = [int(number) for number in page_numbers if number.isdigit()]
    max_page_number = max(filtered_page_numbers)
    return max_page_number

# 从网站中获取所有链接
for num in range(1, 18):
    max_page_number = get_max_page_number(num)
    for page in range(1, max_page_number + 1):
        url = f"https://china.guidechem.com/datacenter/msds_cn_list-{num}-p{page}.html"
        links = get_links(url)
        print(links)
