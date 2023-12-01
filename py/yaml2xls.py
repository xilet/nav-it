
#pip install pyyaml pandas openpyxl
import yaml
import pandas as pd

def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def yaml_to_dataframe(yaml_data):
    rows = []
    id_counter = 1  # 初始化 id 计数器
    for category in yaml_data:
        taxonomy = category['taxonomy']
        icon = category['icon']
        for term_group in category.get('list', []):
            term = term_group['term']
            for link in term_group['links']:
                title = link.get('title', '')
                description = link.get('description', '')
                url = link.get('url', '')
                logo = link.get('logo', '')
                rows.append([id_counter, 1, taxonomy, term, title, description, url, logo, icon])
                id_counter += 1  # 递增 id
    return pd.DataFrame(rows, columns=['id', 'is_use', 'taxonomy', 'term', 'title', 'description', 'url', 'logo', 'icon'])

# YAML 文件路径
yaml_file_path = './../data/webstack.yml'

# 读取 YAML 文件
yaml_data = read_yaml(yaml_file_path)

# 转换为 DataFrame
df = yaml_to_dataframe(yaml_data)

# 输出到 Excel 文件
excel_file_path = './sites.xlsx'
df.to_excel(excel_file_path, index=False)

