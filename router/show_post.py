from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
import certifi

import jwt
import datetime

import hashlib

ca = certifi.where()
client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.YDMD

show_post = Blueprint('show_post', __name__, url_prefix="/show")

SECRET_KEY = 'YDMD'

@show_post.route('/')
def home():

    # return render_template('show_post/index.html')
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        print(user_info['id'])
        return render_template('show_post/index.html', user_id=user_info["id"])
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')


# @show_post.route('/login', methods=['GET'])
# def login():
#     payload = {
#         'id': 'test1',
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
#     }
#     token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
#     return jsonify({'token': token})

@show_post.route('/update', methods=['POST'])
def update():
    user_id = request.form['id']
    dog_name = request.form['dog_name']
    comment = request.form['comment']

    print(user_id, dog_name, comment)
    comments = db.user.find_one({'id': user_id}, {'_id': False})['comments']
    for i in range(len(comments)):
        if comments[i]['dog_name'] == dog_name:
            comments[i]['comment'] = comment

    db.user.update_one({'id': user_id}, {'$set': {'comments': comments}})
    return jsonify({'msg': '수정완료!'})


@show_post.route('/show_post', methods=["GET"])
def show():
    user_id = request.args['user_id']
    dog_name = request.args['dog_name']

    dog = db.dogs.find_one({'dog_name': dog_name}, {'_id': False})

    users = list(db.user.find({}, {'_id': False}))
    comments = db.user.find_one({'id': user_id}, {'_id': False})['comments']

    print(type(dog['dog_name']))
    # print(dog['dog_name'], dog['dog_image'], dog['dog_intro'])

    return jsonify({'msg': '연결 완료!', 'dog': dog, 'comments':comments, 'users':users})

