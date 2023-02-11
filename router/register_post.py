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
    user_name_receive = request.form['user_name_give']
    print(user_name_receive)
    doc = {
        'dog_name': dog_name_receive,
        'comment': comment_receive
    }
    user_comments = db.user.find_one({'id': user_name_receive}, {'_id': False})["comments"]
    user_comments.append(doc)
    db.user.update_one({'id': user_name_receive}, {'$set': {'comments': user_comments}})

    return jsonify({'msg': '작성완료'})


# 글 등록 화면에서 강아지 db 정보 주는 함수
# 클라이언트의 sessionstorage에 저장된 dog_name을 받음
@register_post.route('/api/register_post/dog_info', methods=["POST"])
def dog_info():
    dog_name_receive = request.form['dog_name_give']
    dog = db.dogs.find_one({'dog_name': dog_name_receive}, {'_id': False})
    return jsonify({'dog': dog})
