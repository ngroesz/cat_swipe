from web_service.database import db

class Person(db.Model):
    __tablename__ = 'persons'

    id  = db.Column(db.String, primary_key=True)
    age = db.Column(db.Integer)

    def __repr__(self):
        return "<Person %r>" % self.id
