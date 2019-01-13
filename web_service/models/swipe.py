from web_service.database import db

class Swipe(db.Model):
    __tablename__ = 'swipes'

    id     = db.Column(db.String, primary_key=True)
    age    = db.Column(db.Integer)
    cat_id = db.Column(db.Integer, db.ForeignKey('cats.id', nullable=False)

    def __repr__(self):
        return "<Swipe %r>" % self.id
