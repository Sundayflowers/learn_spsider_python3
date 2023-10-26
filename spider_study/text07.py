import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl  # 用于修改x轴坐标

plt.style.use('ggplot')  # 默认绘图风格
fig = plt.figure(figsize=(8, 5))  # 设置图片大小
colors1 = '#6D6D6D'  # 设置图表title、text标注的颜色

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
try:
    df = pd.read_csv('maoyan_top100.csv', encoding="latin1", header=None, names=columns, index_col='index')
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    df = pd.DataFrame(columns=columns)  # Create an empty DataFrame to avoid errors

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

# 下面是其他分析函数的内容

annalysis_1()
