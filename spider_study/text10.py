import pandas as pd

# 读取原始CSV文件，使用'latin1'编码
with open('maoyan_top100.csv', 'r', encoding='latin1') as file:
    lines = file.readlines()

cleaned_lines = []
for line in lines:
    try:
        line.encode('utf-8').decode('utf-8')
        cleaned_lines.append(line)
    except UnicodeDecodeError:
        print(f"Ignored a line with invalid characters: {line}")

# 将处理后的内容写入新的CSV文件，使用'latin1'编码
with open('cleaned_maoyan_top100.csv', 'w', encoding='latin1') as file:
    file.writelines(cleaned_lines)

# 读取新的CSV文件
columns = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
df = pd.read_csv('cleaned_maoyan_top100.csv', encoding="latin1", header=None, names=columns, index_col='index')
