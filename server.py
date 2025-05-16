import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
from src.models import db, User, Message
from datetime import datetime

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crypText.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Store active users
active_users = {}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('login')
def handle_login(data):
    user_id = data['userId']
    active_users[user_id] = request.sid
    emit('user_online', {'userId': user_id}, broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    try:
        sender_id = data['senderId']
        recipient_id = data['recipientId']
        content = data['content']
        
        print(f"Message from {sender_id} to {recipient_id}: {content}")
        
        # Save message to database
        message = Message(
            sender_id=sender_id,
            recipient_id=recipient_id,
            content=content
        )
        
        with app.app_context():
            db.session.add(message)
            db.session.commit()
        
        # Emit to recipient and sender
        message_data = {
            'senderId': sender_id,
            'content': content,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Send to recipient if online
        if recipient_id in active_users:
            emit('new_message', message_data, room=active_users[recipient_id])
        
        # Send confirmation back to sender
        emit('message_sent', message_data)
        
        return True
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        emit('message_error', {'error': str(e)})
        return False

@socketio.on('disconnect')
def handle_disconnect():
    for user_id, sid in active_users.items():
        if sid == request.sid:
            del active_users[user_id]
            emit('user_offline', {'userId': user_id}, broadcast=True)
            break

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)