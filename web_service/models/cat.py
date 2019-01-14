from web_service.database import db

class Cat(db.Model):
    __tablename__ = 'cats'

    id        = db.Column(db.Integer, primary_key=True)
    age       = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'))


    def __repr__(self):
        return "<Cat %r>" % self.id
