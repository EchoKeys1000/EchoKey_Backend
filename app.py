from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    # phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(200), nullable=False)


@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    # phone = data.get('phone')
    message = data.get('message')

    if not username or not email:
        return jsonify({'error': 'Missing information, name and email are essential.'}), 400

    new_message = UserMessage(username=username, email=email, message=message)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'success': 'Message received'}), 200


@app.route('/')
def index():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
