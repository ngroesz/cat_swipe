from web_service.database import db

class Person(db.Model):
    __tablename__ = 'persons'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age  = db.Column(db.Integer)

    def __repr__(self):
        return "<Person %r>" % self.id
