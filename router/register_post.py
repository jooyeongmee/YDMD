from flask import Blueprint,  render_template, request, jsonify


from pymongo import MongoClient

import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority',  tlsCAFile=ca)
db = client.YDMD.user

register_post = Blueprint('register_post', __name__, url_prefix="/register")

@register_post.route("/")
def home():
    return render_template("index.html")

@register_post.route("/user/login", methods=["POST"])
def sample():
    bucket_receive = request.form['']
    return jsonify({sample: 'sample_list'})

