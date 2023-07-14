'''
Author: Sprite 741935669@qq.com
Date: 2023-07-10 16:56:13
LastEditors: Sprite 741935669@qq.com
LastEditTime: 2023-07-13 14:23:06
FilePath: \undefinedd:\工作相关\数智设计平台资料\业务内容\爬虫\request_chemnet_msds.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import chardet
import time

with open('links.txt', 'r') as file:
    index = 0
    count = 0
    df_all = pd.DataFrame()  # 创建空的DataFrame来保存数据
    folder_path = 'excel_files'  # 设置存放Excel文件的文件夹路径
    os.makedirs(folder_path, exist_ok=True)  # 创建文件夹
    # 逐行读取文件内容
    for line in file:
        link = line.strip()  # 去除行末尾的换行符和空格
        url = "https://cheman.chemnet.com" + link
        print(url)
        # 发送HTTP GET请求获取网页源代码
        response = requests.get(url)
        # 自动检测编码格式
        response.encoding = chardet.detect(response.content)['encoding']
        html_code = response.text
        # 使用BeautifulSoup解析网页源代码
        soup = BeautifulSoup(html_code, 'html.parser')
        # 寻找包含目标信息的<table>标签
        table = soup.find('table')
        if table is None:
            print(f"No table found in {url}, skipping...")
            continue
        # 提取国际标号、中文名称、英文名称等信息
        info = {}
        rows = table.find_all('tr')
        for row in rows:
            tds = row.find_all('td')
            if(tds[0].text.strip() != ''):
                if len(tds) == 4:
                    # 去掉冒号
                    key = tds[0].text.strip().replace('：', '')
                    key = tds[0].text.strip().replace(':', '')
                    value = tds[1].text.strip()
                    info[key] = value
                    if tds[2].text.strip() != '':
                        # 去掉冒号
                        key = tds[2].text.strip().replace('：', '')
                        key = tds[2].text.strip().replace(':', '')
                        value = tds[3].text.strip()
                        info[key] = value
            else:
                break
        # 将数据转换为DataFrame，并添加到总的DataFrame中
        df = pd.DataFrame(info, index=[0])
        df['id'] = url.split('=')[-1]  # 添加id列
        df_all = pd.concat([df_all, df])
        count += 1
        
        # 每100条数据保存为一个Excel文件
        if count % 100 == 0:
            # 拼接文件路径
            file_path = os.path.join(folder_path, f'chemical_info{index}.xlsx')
            # 将数据保存到Excel表格中
            df_all.to_excel(file_path, index=False)
            index += 1
            df_all = pd.DataFrame()  # 清空总的DataFrame
        
        time.sleep(5)  # 暂停5秒，模拟人的行为

    # 对剩余不满100条的数据保存为一个Excel文件
    if count % 100 != 0:
        file_path = os.path.join(folder_path, f'chemical_info{index}.xlsx')
        df_all.to_excel(file_path, index=False)
