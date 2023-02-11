from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for

from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient("mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority",tlsCAFile=ca)
db = client.YDMD

sign_in = Blueprint('signin', __name__, url_prefix="/signin")

SECRET_KEY = 'YDMD'

import jwt

import datetime

import hashlib


@sign_in.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    print(request.cookies.get('mytoken'))
    try:

        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        user_info = db.user.find_one({"id": payload['id']})
        print(user_info)
        return render_template('signin/signin.html', id=user_info["id"])
    except jwt.ExpiredSignatureError:
        return render_template('signin/signin.html')
    except jwt.exceptions.DecodeError:
        return render_template('signin/signin.html')




@sign_in.route('/api/signin', methods=['POST'])
def api_signin():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': id_receive,
        'pw': pw_hash
    }
    result = db.user.find_one(doc)

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@sign_in.route('/api/signup', methods=['POST'])
def api_signup():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    user_ids = list(db.user.find({'id': id_receive}, {'_id': False}))
    if (len(user_ids)) > 0:
        msg = '이미 가입된 아이디입니다. 다른 아이디로 등록해주세요!'
    else:
        msg = 'success'

    doc = {
        'id': id_receive,
        'pw': pw_hash,
        'comments': []
    }
    db.user.insert_one(doc)

    return jsonify({'result': msg})


@sign_in.route('/api/id', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])


        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'id': userinfo['id']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
