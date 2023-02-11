from flask import Blueprint, request, render_template, jsonify



from pymongo import MongoClient

client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority')
dog_db = client.YDMD.dogs

import requests
from bs4 import BeautifulSoup

main = Blueprint('main', __name__, url_prefix="/main")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 메인페이지에 보여줄 강아지 목록
our_dogs = {'말티즈', '푸들', '골든 리트리버'}

@main.route('/', methods=["GET"])
def home():
    return render_template("index.html")


@main.route("/api/dog-list", methods=["GET"])
def get_dog_list():
    dog_list = list()
    for category in categories:
        cat_data = requests.get(category, headers=headers)
        cat_soup = BeautifulSoup(cat_data.text, 'html.parser')
        dogs = cat_soup.select('main > section > div > div > div:nth-child(2) > div:nth-child(1) > '
                               'div.rc-padding-y--sm > div.rc-layout-container.rc-content-card.rc-match-heights > '
                               'div')
        print(dogs)
        idx = 0
        for dog in dogs:
            dog_url = dog.select_one('a')['href']
            dog_name = dog.select_one('h3').text
            if dog_name in our_dogs and idx < len(our_dogs):  # 등록할 강아지가 리스트에 있으면 소개 페이지 크롤링
                dog_data = requests.get(dog_url, headers=headers)
                dog_soup = BeautifulSoup(dog_data.text, 'html.parser')
                dog_image = \
                    dog_soup.select_one('body > main > div.rc-bg-colour--brand3.rc-padding--sm.rc-padding-y--none.rc'
                                        '-margin-bottom--xs.rc-margin-bottom--sm--mobile > '
                                        'div.rc-layout-container.rc-two-column.rc-reverse-layout-mobile.rc-content-h'
                                        '-middle.rc-max-width--xl > div.rc-column.rc-padding-bottom--none > picture > '
                                        'img')['data-srcset'].split()[0]
                dog_intro = dog_soup.select_one('main > div:nth-child(3) > '
                                                'div.rc-layout-container.rc-three-column.rc-max-width--xl > '
                                                'div:nth-child(1)'
                                                '> p:nth-child(2)').text
                idx += 1
                doc = {
                    'dog_name': dog_name,
                    'dog_image': dog_image,
                    'dog_intro': dog_intro
                }
                dog_list.append(doc)
                print(dog_list)
            elif idx >= len(our_dogs):
                break
    return jsonify({'dog_list': dog_list})



