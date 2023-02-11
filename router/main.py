from flask import Blueprint, request, render_template, jsonify, redirect, url_for

from pymongo import MongoClient

import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

dog_db = client.YDMD.dogs
url_db = client.YDMD.english_url
user_db = client.YDMD.user

import requests
from bs4 import BeautifulSoup

import jwt

import hashlib

# 보안 상 시크릿키는 길게, 복잡하게 만들고 공유 금지해야 함
# 생성용 키/검증용 키 두 개로 운용
SECRET_KEY = 'YDMD'

main = Blueprint('main', __name__, url_prefix="/")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 메인페이지에 보여줄 강아지 목록 - 원하는 종 생길 때 수작업 추가
our_dogs = {'말티즈', '푸들', '골든 리트리버', '포메라니안', '시츄', '요크셔테리어', '닥스훈트'}
dog_list = list()
for dog_name in our_dogs:
    dog_info = url_db.find_one({'dog_name': dog_name})
    if dog_info is not None:
        dog_url = dog_info['eng_url']
        dog_data = requests.get(dog_url, headers=headers)
        dog_soup = BeautifulSoup(dog_data.text, 'html.parser')
        dog_image = dog_info['dog_image']
        dog_intro = dog_soup.select_one('main > div:nth-child(3) > '
                                        'div.rc-layout-container.rc-three-column.rc-max-width--xl > '
                                        'div:nth-child(1)'
                                        '> p').text
        doc = {
            'dog_name': dog_name,
            'dog_image': dog_image,
            'dog_intro': dog_intro
        }
        filter_val = {'dog_name': dog_name}
        operator_val = {'$set': {"dog_name": dog_name,
                                 "dog_image": dog_image,
                                 "dog_intro": dog_intro}}
        dog_db.update_one(filter_val, operator_val, upsert=True)
        dog_list.append(doc)
    else:
        print("강아지 이름을 찾을 수 없음")


# 메인페이지는 토큰 받아서 검증 후 만료됐거나 일치하지 않으면 logout 결과값 보냄
@main.route('/', methods=["GET"])
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = user_db.find_one({"id": payload['id']})
        # 토큰이 유효한데 db에 유저가 삭제되면 find_one이 null이 되면서 TypeError 발생
        if user_info is None:
            return render_template('/index.html', result="logout")
        else:
            return render_template('/index.html', result="login", id=user_info['id'])
    except jwt.ExpiredSignatureError:
        return render_template('/index.html', result="logout")
    except jwt.exceptions.DecodeError:
        return render_template('/index.html', result="logout")


@main.route("/api/dog-list", methods=["GET"])
def get_dog_list():
    dogs = list(dog_db.find({}, {'_id': False}))
    return jsonify({'dogs': dogs})
