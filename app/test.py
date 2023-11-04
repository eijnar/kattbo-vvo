from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to your secret key

jwt = JWTManager(app)

@app.route('/')
def create_token():
    access_token = create_access_token(identity='example_user')
    return jsonify(access_token=access_token)

if __name__ == '__main__':
    app.run()