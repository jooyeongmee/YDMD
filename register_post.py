from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority',  tlsCAFile=ca)
db = client.YDMD.user

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/user/login", methods=["POST"])
def sample():
    bucket_receive = request.form['']
    return jsonify({sample: sample_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)