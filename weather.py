# 导入工具库
import requests  # 用于获取网页内容
from bs4 import BeautifulSoup  # 用于解析网页
import pandas as pd  # 用于保存到Excel

# 1. 获取网页内容（模拟浏览器访问）
url = "http://www.weather.com.cn/weather/101270101.shtml"  # 修正 URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # 解决中文乱码

# 2. 检查是否获取成功
if response.status_code != 200:
    print("网页访问失败！请检查网络或网址")
    exit()

# 3. 解析网页
soup = BeautifulSoup(response.text, 'html.parser')

# 通过浏览器开发者工具找到天气数据所在的HTML标签
weather_data = soup.find('ul', class_='t clearfix')  # 找到包含天气的<ul>标签
if not weather_data:
    print("未找到天气数据，请检查网页结构是否变化")
    exit()

days = weather_data.find_all('li')  # 获取每一天的<li>标签

# 4. 提取数据到列表
weather_list = []
for day in days:
    # 提取日期（如"13日（今天）"）
    date = day.find('h1').text.strip() if day.find('h1') else "日期未知"
    # 提取天气状况（如"多云"）
    weather = day.find('p', class_='wea').text.strip() if day.find('p', class_='wea') else "天气未知"
    # 提取温度（如"15/20℃"）
    temp = day.find('p', class_='tem').text.replace('\n', '').strip() if day.find('p', class_='tem') else "温度未知"

    weather_list.append([date, weather, temp])

# 5. 保存到Excel
df = pd.DataFrame(weather_list, columns=['日期', '天气', '温度'])
df.to_excel('成都天气.xlsx', index=False)
print("数据已保存到 成都天气.xlsx！")
