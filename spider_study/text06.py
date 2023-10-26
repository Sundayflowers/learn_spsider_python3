import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl  # 用于修改x轴坐标

plt.style.use('ggplot')  # 默认绘图风格
fig = plt.figure(figsize=(8, 5))  # 设置图片大小
colors1 = '#6D6D6D'  # 设置图表title、text标注的颜色

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
try:
    df = pd.read_csv('maoyan_top100.csv', encoding="utf-8", header=None, names=columns, index_col='index')
except UnicodeDecodeError:
    # If you encounter a decoding error, try using a different encoding (e.g., latin1)
    df = pd.read_csv('maoyan_top100.csv', encoding='latin1', header=None, names=columns, index_col='index')

def annalysis_1():
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

def annalysis_2():
    area_count = df.groupby(by='area').area.count().sort_values(ascending=False)

    area_count.plot.bar(color='#4652B1')
    pl.xticks(rotation=0)

    for x, y in enumerate(list(area_count.values)):
        plt.text(x, y + 0.5, '%s' % round(y, 1), ha='center', color=colors1)
    plt.title('各国/地区电影数量排名', color=colors1)
    plt.xlabel('国家/地区')
    plt.ylabel('数量(部)')
    plt.show()

def annalysis_3():
    df['year'] = df['time'].str.split('/').str[0]

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

def annalysis_4():
    starlist = df.star.str.replace(' ', '').str.split(',').explode().dropna()

    star_counts = starlist.value_counts().head(10)

    x_star = star_counts.index
    y_star = star_counts.values

    plt.bar(range(10), y_star, tick_label=x_star)
    pl.xticks(rotation=270)
    for x, y in enumerate(y_star):
        plt.text(x, y + 0.1, '%s' % round(y, 1), ha='center', color=colors1)

    plt.title('演员电影作品数量排名', color=colors1)
    plt.xlabel('演员')
    plt.ylabel('数量(部)')
    plt.tight_layout()
    plt.show()

annalysis_1()
