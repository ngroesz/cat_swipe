from web_service.database import db

class Cat(db.Model):
    __tablename__ = 'cats'

    id        = db.Column(db.String, primary_key=True)
    age       = db.Column(db.Integer)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id', nullable=False))

    def __repr__(self):
        return "<Cat %r>" % self.id
