from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    display_name = db.Column(db.String(50), nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Add relationship to chats
    sent_messages = db.relationship('Chat', backref='sender', foreign_keys='Chat.sender_id')
    received_messages = db.relationship('Chat', backref='recipient', foreign_keys='Chat.recipient_id')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(6), db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.String(6), db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    
    # Add relationship to users
    sender = db.relationship('User', foreign_keys=[sender_id])
    recipient = db.relationship('User', foreign_keys=[recipient_id])

from .chat import Chat