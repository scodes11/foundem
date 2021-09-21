from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Lost(db.Model):
    type = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    # date=db.Column(db.DateTime, default= datetime.utcnow)
    img = db.Column(db.LargeBinary, nullable=False)
    # img_name = db.Column(db.String(50), nullable=False)
    # mimetype=db.Column(db.Text,nullable=False)
    location = db.Column(db.String(200), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    number = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"{self.type}-{self.brand}-{self.color}-{self.img}-{self.location}-{self.code}-{self.name}-{self.number}-{self.email}"


