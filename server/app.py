from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        return jsonify([message.to_dict() for message in messages]),200
    elif request.method == 'POST':
        new_message = Message(
            body= request.json.get("body"),
            username= request.json.get("username")
        )

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            message_dict,
            201
        )

        return response
    


@app.route('/messages/<int:id>', methods=['GET','PATCH', 'DELETE'])
def messages_by_id(id):
    
    message = Message.query.get(id)

    if message is None:
        return jsonify({'error': 'Message not found'}), 404

    if request.method == 'GET':
        return jsonify(message.to_dict()), 200

    elif request.method == 'PATCH':
        body = request.json.get("body")
        if body:
            message.body = body

        db.session.commit()

        return jsonify(message.to_dict()), 200
        
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        return jsonify({'message': 'Message deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555)
