from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = db.Column(db.String(50), nullable=False)
    sender_number = db.Column(db.String(15), nullable=False)
    receiver_number = db.Column(db.String(15), nullable=False)

    def to_dict(self):
        return {
            "account_id": self.account_id,
            "message_id": self.id,
            "sender_number": self.sender_number,
            "receiver_number": self.receiver_number
        }

