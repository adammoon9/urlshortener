from app.extensions import db
from datetime import datetime as dt

class URL(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    shortCode = db.Column(db.String(12), unique=True)
    createdAt = db.Column(db.DateTime, nullable=False, default=dt.now())
    updatedAt = db.Column(db.DateTime, nullable=True, default=dt.now())
    accessCount = db.Column(db.Integer, default=0)

    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'shortCode': self.shortCode,
            'createdAt': self.createdAt.strftime('%d/%m/%Y - %H:%M:%S'),
            'updatedAt': self.updatedAt.strftime('%d/%m/%Y - %H:%M:%S') if self.updatedAt is not None else 'This URL has not been updated or accessed yet.'
        }