# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool

# 定义请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}

# 获取网页内容
def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None

# 解析页面，使用Beautiful Soup
def parse_one_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('dd')
    for item in items:
        yield {
            'index': item.find('i', class_='board-index').text,
            'thumb': item.find('img', class_='board-img')['data-src'],
            'name': item.find('p', class_='name').a.text,
            'star': item.find('p', class_='star').text.strip()[3:],
            'time': get_release_time(item.find('p', class_='releasetime').text.strip()[5:]),
            'area': get_release_area(item.find('p', class_='releasetime').text.strip()[5:]),
            'score': item.find('p', class_='score').i.text + item.find_all('p', class_='score')[1].i.text
        }

# 提取时间函数
def get_release_time(data):
    pattern = re.compile(r'(.*?)(\(|$)')
    items = re.search(pattern, data)
    if items:
        return items.group(1)
    return '未知'

# 提取国家函数
def get_release_area(data):
    pattern = re.compile(r'.*\((.*)\)')
    items = re.search(pattern, data)
    if items:
        return items.group(1)
    return '未知'

# 数据存储到CSV文件
def write_to_csv(items):
    with open('猫眼top100.csv', 'a', encoding='utf_8_sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(items.values())

# 封面下载
def download_thumb(name, url, num):
    try:
        response = requests.get(url)
        with open('封面图/' + name + '.jpg', 'wb') as f:
            f.write(response.content)
            print('第%s部电影封面下载完毕' % num)
    except requests.RequestException as e:
        print(e)

# 主程序
def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_csv(item)
        download_thumb(item['name'], item['thumb'], item['index'])

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(1)])
