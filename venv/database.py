from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, timezone

db = SQLAlchemy()

def init_db(app: Flask):
    if 'SQLALCHEMY_DATABASE_URI' not in app.config:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///infoleak.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

class DadosColetados(db.Model):
    __tablename__ = 'dadoscoletados'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable = False)
    senha = db.Column(db.String(100), nullable = False)
    origem_ip = db.Column(db.String(45), nullable = False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


    def __repr__(self):
        return f'<Dadoscoletados id={self.id} user={self.user}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user,
            'senha': self.senha,
            'origem_ip': self.origem_ip,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }