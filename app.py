from flask import Flask, render_template

# router
from router import main, register_post, show_post, signin

app = Flask(__name__)

# blueprints
app.register_blueprint(main.main)
app.register_blueprint(register_post.register_post)
app.register_blueprint(show_post.show_post)
app.register_blueprint(signin.sign_in)


# GET: 홈페이지
@app.route('/', methods=['GET'])
def home():
    return render_template('signin/signin.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)