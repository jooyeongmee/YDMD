from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import certifi

app = Flask(__name__)

ca = certifi.where()
client = MongoClient('mongodb+srv://project:ydmd5@cluster0.n7giicj.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.YDMD


@app.route('/')
def home():
    return render_template('show_post/index.html')

@app.route('/show_post', methods=["GET"])
def show():
    # user_id = request.args['user_id']
    dog_name = request.args['dog_name']

    dog = db.dogs.find_one({'dog_name': dog_name}, {'_id': False})
    print(dog['dog_name'], dog['dog_image'], dog['dog_intro'])
    return jsonify({'msg': '연결 완료!', 'dog': dog})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)