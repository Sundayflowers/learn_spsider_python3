import requests
import re
from bs4 import BeautifulSoup
import csv
from multiprocessing import Pool
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl

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
        index = item.find('i', class_='board-index').text
        thumb = item.find('img', class_='board-img')['data-src']
        name = item.find('p', class_='name').a.text
        star = item.find('p', class_='star').text.strip()[3:]
        releasetime = item.find('p', class_='releasetime').text.strip()[5:]
        time = get_release_time(releasetime)
        area = get_release_area(releasetime)

        score_elements = item.find_all('p', class_='score')
        if len(score_elements) >= 2:
            score = score_elements[0].i.text + score_elements[1].i.text
        else:
            score = 'N/A'  # 设置默认值

        yield {
            'index': index,
            'thumb': thumb,
            'name': name,
            'star': star,
            'time': time,
            'area': area,
            'score': score
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
    with open('maoyan_top100.csv', 'a', encoding='utf_8_sig', newline='') as f:
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

# 可视化分析
# -----------------------------------------------------------------------------
# 1电影评分最高top10
def annalysis_1():
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(8, 5))
    colors1 = '#6D6D6D'

    columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
    df = pd.read_csv('maoyan_top100.csv', encoding="utf-8", index_col='index')

    df_score = df.sort_values('score', ascending=False)
    name1 = df_score.name[:10]
    score1 = df_score.score[:10]
    plt.bar(range(10), score1, tick_label=name1)
    plt.ylim((9, 9.8))
    plt.title('电影评分最高top10', color=colors1)
    plt.xlabel('电影名称')
    plt.ylabel('评分')

    for x, y in enumerate(list(score1)):
        plt.text(x, y + 0.01, '%s' % round(y, 1), ha='center', color=colors1)

    pl.xticks(rotation=270)
    plt.tight_layout()
    plt.show()

# 2各国家的电影数量比较
def annalysis_2():
    columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
    df = pd.read_csv('maoyan_top100.csv', encoding="utf-8", index_col='index')

    area_count = df['area'].value_counts()

    area_count.plot.bar(color='#4652B1')
    pl.xticks(rotation=0)

    for x, y in enumerate(list(area_count.values)):
        plt.text(x, y + 0.5, '%s' % round(y, 1), ha='center', color=colors1)
    plt.title('各国/地区电影数量排名', color=colors1)
    plt.xlabel('国家/地区')
    plt.ylabel('数量(部)')
    plt.show()

# 3电影作品数量集中的年份
# 从日期中提取年份
def annalysis_3():
    columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
    df = pd.read_csv('maoyan_top100.csv', encoding="utf-8", index_col='index')
    df['year'] = df['time'].map(lambda x: x.split('/')[0])

    grouped_year = df.groupby('year')
    grouped_year_amount = grouped_year.year.count()
    top_year = grouped_year_amount.sort_values(ascending=False)

    top_year.plot(kind='bar', color='orangered')
    for x, y in enumerate(list(top_year.values)):
        plt.text(x, y + 0.1, '%s' % round(y, 1), ha='center', color=colors1)
    plt.title('电影数量年份排名', color=colors1)
    plt.xlabel('年份(年)')
    plt.ylabel('数量(部)')

    plt.tight_layout()
    plt.show()

# 4拥有电影作品数量最多的演员
def annalysis_4():
    columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
    df = pd.read_csv('maoyan_top100.csv', encoding="utf-8", index_col='index')

    starlist = []
    star_total = df.star
    for i in df.star.str.replace(' ', '').str.split(','):
        starlist.extend(i)

    starall = set(starlist)
    starall2 = {}
    for i in starall:
        if starlist.count(i) > 1:
            starall2[i] = starlist.count(i)

    starall2 = sorted(starall2.items(), key=lambda starlist: starlist[1], reverse=True)
    starall2 = dict(starall2[:10])

    x_star = list(starall2.keys())
    y_star = list(starall2.values())

    plt.bar(range(10), y_star, tick_label=x_star)
    pl.xticks(rotation=270)
    for x, y in enumerate(y_star):
        plt.text(x, y + 0.1, '%s' % round(y, 1), ha='center', color=colors1)

    plt.title('演员电影作品数量排名', color=colors1)
    plt.xlabel('演员')
    plt.ylabel('数量(部)')
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i * 10 for i in range(1)])

    annalysis_1()
    annalysis_2()
    annalysis_3()
    annalysis_4()
