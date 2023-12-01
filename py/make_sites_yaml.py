import pandas as pd
import yaml

# 读取数据并筛选
df = pd.read_excel("sites.xlsx")
df = df[df["is_use"] == 1]

# 构建 taxonomy 和 icon 的映射
taxonomy_icon_dict = df.drop_duplicates('taxonomy').set_index('taxonomy')['icon'].to_dict()

# 构建一级菜单
all_list = [{'taxonomy': taxonomy, 'icon': icon, 'list': []} 
            for taxonomy, icon in taxonomy_icon_dict.items()]

# 构建二级菜单项
for term, group in df.groupby('term'):
    links = group[['title', 'logo', 'url', 'description']].to_dict(orient='records')
    term_item = {'term': term, 'links': links}
    
    # 找到对应的一级菜单并添加
    taxonomy = group['taxonomy'].iloc[0]
    for item in all_list:
        if item['taxonomy'] == taxonomy:
            item['list'].append(term_item)
            break

# 输出到 YAML
with open("webstack.yml", 'w', encoding="utf8") as f:
    yaml.dump(all_list, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

