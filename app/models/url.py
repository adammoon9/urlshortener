from app.extensions import db
from datetime import datetime as dt

class URL(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    shortCode = db.Column(db.String(12))
    createdAt = db.Column(db.DateTime, nullable=False, default=dt.now)
    updatedAt = db.Column(db.DateTime, nullable=True, onupdate=dt.now)
    accessCount = db.Column(db.Integer, default=0)

    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'shortCode': self.shortCode,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }