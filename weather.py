import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.weather.com.cn/weather/101270101.shtml"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

if response.status_code != 200:
    print("网页访问失败！请检查网络或网址")
    exit()

soup = BeautifulSoup(response.text, 'html.parser')

weather_data = soup.find('ul', class_='t clearfix')
if not weather_data:
    print("未找到天气数据，请检查网页结构是否变化")
    exit()

days = weather_data.find_all('li')
weather_list = []

for day in days:
    date = day.find('h1').text.strip() if day.find('h1') else "日期未知"
    weather = day.find('p', class_='wea').text.strip() if day.find('p', class_='wea') else "天气未知"
    temp = day.find('p', class_='tem').text.replace('\n', '').strip() if day.find('p', class_='tem') else "温度未知"

    weather_list.append([date, weather, temp])

df = pd.DataFrame(weather_list, columns=['日期', '天气', '温度'])

df.to_csv('成都天气.csv', index=False, encoding='utf-8')
print("数据已保存到 成都天气.csv！")