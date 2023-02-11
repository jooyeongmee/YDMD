from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
from pymongo import MongoClient
import certifi

import jwt


ca = certifi.where()
client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.YDMD

show_post = Blueprint('show_post', __name__, url_prefix="/show")

SECRET_KEY = 'YDMD'

@show_post.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        # 토큰이 유효한데 db에 유저가 삭제되면 find_one이 null이 되면서 TypeError 발생
        if user_info is None:
            return render_template('/index.html', result="logout")
        else:
            return render_template('show_post/index.html', result="login",
                                   id=user_info['id'])
    except jwt.ExpiredSignatureError:
        return render_template('/index.html', result="logout")
    except jwt.exceptions.DecodeError:
        return render_template('/index.html', result="logout")


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


@show_post.route('/delete', methods=['DELETE'])
def delete():
    user_id = request.form['id']
    dog_name = request.form['dog_name']
    comment = request.form['comment']

    print(user_id, dog_name, comment)
    comments = db.user.find_one({'id': user_id}, {'_id': False})['comments']
    for i in range(len(comments)):
        if comments[i]['dog_name'] == dog_name and comments[i]['comment'] == comment:
            del comments[i]

    db.user.update_one({'id': user_id}, {'$set': {'comments': comments}})
    return jsonify({'msg': '삭제완료!'})


@show_post.route('/show_post', methods=["GET"])
def show():
    user_id = request.args['user_id']
    dog_name = request.args['dog_name']

    dog = db.dogs.find_one({'dog_name': dog_name}, {'_id': False})

    users = list(db.user.find({}, {'_id': False}))
    comments = db.user.find_one({'id': user_id}, {'_id': False})['comments']

    return jsonify({'dog': dog, 'comments':comments, 'users':users})

