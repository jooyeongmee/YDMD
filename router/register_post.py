from flask import Blueprint,  render_template, request, jsonify


from pymongo import MongoClient

import certifi

ca = certifi.where()
client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority',  tlsCAFile=ca)
db = client.YDMD

register_post = Blueprint('register_post', __name__, url_prefix="/register")

@register_post.route("/")
def home():
    return render_template('register_post/register_post.html')

@register_post.route("/register_post", methods=["POST"])
def comment_post():
    comment_receive = request.form['comment_give']
    dog_name_receive = request.form['dog_name_give']
    id='test1'

    doc = {
        'dog_name':dog_name_receive,
        'comment': comment_receive
    }
    users = db.user.find_one({'id':id},{'_id':False})["comments"]
    users.append(doc)
    db.user.update_one({'id':id},{'$set': {'comments':users}})

    print(users)
    return jsonify({'msg': '작성완료'})


# @register_post.route("/register_post", methods=["GET"])
# def bucket_get():
#     buckets_list = list(db.bucketver2.find({}, {'_id': False}))
#     return jsonify({'buckets': buckets_list})