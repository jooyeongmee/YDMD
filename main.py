import requests
from bs4 import BeautifulSoup

url = 'https://www.royalcanin.com/kr/dogs/breeds/breed-library'

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

bs = BeautifulSoup(data.text, 'html.parser')
# print(bs)
names = bs.select('h3', attrs={'class': 'rc-card__title'})
for name in names:
    print(name.text)



