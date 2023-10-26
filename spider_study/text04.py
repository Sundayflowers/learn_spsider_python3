# 可视化分析
# -----------------------------------------------------------------------------
# 1电影评分最高top10
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl  #用于修改x轴坐标


plt.style.use('ggplot')   #默认绘图风格很难看，替换为好看的ggplot风格
fig = plt.figure(figsize=(8,5))   #设置图片大小
colors1 = '#6D6D6D'  #设置图表title、text标注的颜色

columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']  #设置表头
df = pd.read_csv('maoyan_top100.csv',encoding = "utf-8",header = None,names =columns,index_col = 'index')  #打开表格
# # index_col = 'index' 将索引设为index

def annalysis_1():
    df_score = df.sort_values('score',ascending = False)  #按得分降序排列

    name1 = df_score.name[:10]      #x轴坐标
    score1 = df_score.score[:10]    #y轴坐标
    plt.bar(range(10),score1,tick_label = name1)  #绘制条形图，用range()能搞保持x轴正确顺序
    plt.ylim ((9,9.8))  #设置纵坐标轴范围
    plt.title('电影评分最高top10',color = colors1) #标题
    plt.xlabel('电影名称')      #x轴标题
    plt.ylabel('评分')          #y轴标题

    # 为每个条形图添加数值标签
    for x,y in enumerate(list(score1)):
        plt.text(x,y+0.01,'%s' %round(y,1),ha = 'center',color = colors1)

    pl.xticks(rotation=270)   #x轴名称太长发生重叠，旋转为纵向显示
    plt.tight_layout()    #自动控制空白边缘，以全部显示x轴名称
    # plt.savefig('电影评分最高top10.png')   #保存图片
    plt.show()



# ------------------------------
# 2各国家的电影数量比较
def annalysis_2():
    area_count = df.groupby(by = 'area').area.count().sort_values(ascending = False)

    # 绘图方法1
    area_count.plot.bar(color = '#4652B1')  #设置为蓝紫色
    pl.xticks(rotation=0)   #x轴名称太长重叠，旋转为纵向


    # 绘图方法2
    # plt.bar(range(11),area_count.values,tick_label = area_count.index)

    for x,y in enumerate(list(area_count.values)):
        plt.text(x,y+0.5,'%s' %round(y,1),ha = 'center',color = colors1)
    plt.title('各国/地区电影数量排名',color = colors1)
    plt.xlabel('国家/地区')
    plt.ylabel('数量(部)')
    plt.show()
# plt.savefig('各国(地区)电影数量排名.png')


# ------------------------------
# 3电影作品数量集中的年份
# 从日期中提取年份
def annalysis_3():
    df['year'] = df['time'].map(lambda x:x.split('/')[0])
    # print(df.info())
    # print(df.head())

    # 统计各年上映的电影数量
    grouped_year = df.groupby('year')
    grouped_year_amount = grouped_year.year.count()
    top_year = grouped_year_amount.sort_values(ascending = False)


    # 绘图
    top_year.plot(kind = 'bar',color = 'orangered') #颜色设置为橙红色
    for x,y in enumerate(list(top_year.values)):
        plt.text(x,y+0.1,'%s' %round(y,1),ha = 'center',color = colors1)
    plt.title('电影数量年份排名',color = colors1)
    plt.xlabel('年份(年)')
    plt.ylabel('数量(部)')

    plt.tight_layout()
    # plt.savefig('电影数量年份排名.png')

    plt.show()

# ------------------------------
# 4拥有电影作品数量最多的演员
#表中的演员位于同一列，用逗号分割符隔开。需进行分割然后全部提取到list中
def annalysis_4():
    starlist = []
    star_total = df.star
    for i in df.star.str.replace(' ','').str.split(','):
        starlist.extend(i)
    # print(starlist)
    # print(len(starlist))

    # set去除重复的演员名
    starall = set(starlist)
    # print(starall)
    # print(len(starall))

    starall2 = {}
    for i in starall:
        if starlist.count(i)>1:
            # 筛选出电影数量超过1部的演员
            starall2[i] = starlist.count(i)

    starall2 = sorted(starall2.items(),key = lambda starlist:starlist[1] ,reverse = True)

    starall2 = dict(starall2[:10])  #将元组转为字典格式

    # 绘图
    x_star = list(starall2.keys())      #x轴坐标
    y_star = list(starall2.values())    #y轴坐标

    plt.bar(range(10),y_star,tick_label = x_star)
    pl.xticks(rotation = 270)
    for x,y in enumerate(y_star):
        plt.text(x,y+0.1,'%s' %round(y,1),ha = 'center',color = colors1)

    plt.title('演员电影作品数量排名',color = colors1)
    plt.xlabel('演员')
    plt.ylabel('数量(部)')
    plt.tight_layout()
    plt.show()
# plt.savefig('演员电影作品数量排名.png')

annalysis_1()