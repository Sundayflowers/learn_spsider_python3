import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl

plt.style.use('ggplot')
fig = plt.figure(figsize=(8, 5))
colors1 = '#6D6D6D'

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
df = pd.read_csv('maoyan_top100.csv', encoding="utf-8", header=None, names=columns, index_col='index')

def analysis_1():
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

def analysis_2():
    area_count = df['area'].value_counts().sort_values(ascending=False)

    area_count.plot.bar(color='#4652B1')
    pl.xticks(rotation=0)

    for x, y in enumerate(list(area_count.values)):
        plt.text(x, y + 0.5, '%s' % round(y, 1), ha='center', color=colors1)
    plt.title('各国/地区电影数量排名', color=colors1)
    plt.xlabel('国家/地区')
    plt.ylabel('数量(部)')
    plt.show()

def analysis_3():
    df['year'] = df['time'].str.split('/').str[0]

    grouped_year = df.groupby('year')
    grouped_year_amount = grouped_year.size()
    top_year = grouped_year_amount.sort_values(ascending=False)

    top_year.plot(kind='bar', color='orangered')
    for x, y in enumerate(list(top_year.values)):
        plt.text(x, y + 0.1, '%s' % round(y, 1), ha='center', color=colors1)
    plt.title('电影数量年份排名', color=colors1)
    plt.xlabel('年份(年)')
    plt.ylabel('数量(部)')
    plt.tight_layout()
    plt.show()

def analysis_4():
    starlist = [star.strip() for stars in df.star.str.split(',') for star in stars]

    star_count = pd.Series(starlist).value_counts()
    star_count = star_count[star_count > 1][:10]

    x_star = list(star_count.index)
    y_star = list(star_count.values)

    plt.bar(range(10), y_star, tick_label=x_star)
    pl.xticks(rotation=270)
    for x, y in enumerate(y_star):
        plt.text(x, y + 0.1, '%s' % round(y, 1), ha='center', color=colors1)

    plt.title('演员电影作品数量排名', color=colors1)
    plt.xlabel('演员')
    plt.ylabel('数量(部)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analysis_1()
    analysis_2()
    analysis_3()
    analysis_4()
