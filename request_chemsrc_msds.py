import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import chardet
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}
print('开始爬取数据...')


# 读取链接文件
with open('src_links.txt', 'r') as file:
    index = 0
    count = 0
    not_found_count = 0  # 计数器初始化为0
    folder_path = 'src_excel_files'  # 设置存放Excel文件的文件夹路径
    os.makedirs(folder_path, exist_ok=True)  # 创建文件夹
    df_all = pd.DataFrame()  # 初始化一个空的DataFrame

    # 遍历链接文件中的每一行
    for line in file:
        link = line.strip()  # 去除行末尾的换行符和空格
        url = 'https://www.chemsrc.com'+link
        # print(url)
        # 发送HTTP GET请求获取网页源代码
        response = requests.get(url, headers=headers)

        # 自动检测编码格式
        response.encoding = chardet.detect(response.content)['encoding']
        html_code = response.text

        # 使用BeautifulSoup解析网页源代码
        soup = BeautifulSoup(html_code, 'html.parser')
        row_data = {}

        name_div = soup.find("div", {"id": "nameDiv"})
        if name_div:  # 检查是否成功找到目标元素
            td_list = name_div.find_all("td")
            for td in td_list:
                key = td.find_previous_sibling("th").get_text(strip=True)
                value = td.get_text(strip=True)
                row_data[key] = value
        
        wu_hua_div = soup.find("div", {"id": "wuHuaDiv"})
        if wu_hua_div:  # 检查是否成功找到目标元素
            td_list = wu_hua_div.find_all("td")
            for td in td_list:
                key = td.find_previous_sibling("th").get_text(strip=True)
                value = td.get_text(strip=True)
                row_data[key] = value
        else:
            not_found_count += 1  # 计数器加1
            with open('not_found.txt', 'a') as f:
                f.write(line)
            # 连续超过200个报错那么说明Ip被暂时封了
            if not_found_count>=50:
                break

        not_found_count = 0  # 重置计数器

        df = pd.DataFrame(row_data, index=[0])
        df_all = pd.concat([df_all, df])
        # 增加计数器
        count += 1
        if(count>=5):
            break

        # 每200条数据保存为一个Excel文件
        if count % 2000 == 0:
            # 拼接文件路径
            file_path = os.path.join(folder_path, f'src_msds_{index}.xlsx')
            # 将数据保存到Excel表格中
            df_all.to_excel(file_path, index=False)
            index += 1
            df_all = pd.DataFrame()  # 清空总的DataFrame
        
        time.sleep(2)  # 暂停2秒，模拟人的行为

    # 对剩余不满200条的数据保存为一个Excel文件
    if count % 2000 != 0:
        file_path = os.path.join(folder_path, f'src_msds_{index}.xlsx')
        df_all.to_excel(file_path, index=False)
    
    print('数据爬取完成！')
