from flask import Blueprint, render_template, request, jsonify

from pymongo import MongoClient

import certifi

import jwt
SECRET_KEY = 'YDMD'

ca = certifi.where()
client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.YDMD

register_post = Blueprint('register_post', __name__, url_prefix="/register")


@register_post.route("/")
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        # 토큰이 유효한데 db에 유저가 삭제되면 find_one이 null이 되면서 TypeError 발생
        if user_info is None:
            return render_template('/index.html', result="logout")
        else:
            return render_template('register_post/register_post.html', result="login",
                                   id=user_info['id'])
    except jwt.ExpiredSignatureError:
        return render_template('/index.html', result="logout")
    except jwt.exceptions.DecodeError:
        return render_template('/index.html', result="logout")


@register_post.route("/register_post", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    dog_name_receive = request.form['dog_name_give']
    id = 'test1'

    doc = {
        'dog_name': dog_name_receive,
        'comment': comment_receive
    }
    users = db.user.find_one({'id': id}, {'_id': False})["comments"]
    users.append(doc)
    db.user.update_one({'id': id}, {'$set': {'comments': users}})

    print(users)
    return jsonify({'msg': '작성완료'})


@register_post.route('api/register_post/dog_info', methods=["GET"])
def dog_info():
    dog_name_receive = request.form['dog_give']
    print("dog_name_receive : "+dog_name_receive)
    dog = db.dogs.find({'dog_name': dog_name_receive}, {'_id': False})
    return jsonify({'dog': dog})
