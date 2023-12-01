#pip install pandas openpyxl requests pillow
import os
import shutil
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse
import pandas as pd

def download_and_save_icon(url, filename, proxies=None):
    try:
        result = urlparse(url)
        ico_url = result.scheme + "://" + result.netloc + "/favicon.ico"
        response = requests.get(ico_url, proxies=proxies)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image.save(filename)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

# 读取 Excel 文件
excel_file_path = 'path/to/your/excel/file.xlsx'  # 替换为您的 Excel 文件路径
df = pd.read_excel(excel_file_path)

# 创建 SiteLogo 目录（如果不存在）
if not os.path.exists('SiteLogo'):
    os.makedirs('SiteLogo')

for i, row in df.iterrows():
    title = row['title'].replace(' ', '-')  # 将空格替换为短横线
    url = row['url']
    logo_path = f'SiteLogo/{title}.ico'
    if not os.path.exists(logo_path):
        success = download_and_save_icon(url, logo_path)
        if not success:
            # 使用默认图标替换失败的下载
            shutil.copy('SiteLogo/default.ico', logo_path)
