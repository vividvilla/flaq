from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    email = db.Column(db.String(100), unique = True)
    real_name = db.Column(db.String(100))
    website = db.Column(db.String(100))
    bio = db.Column(db.Text)

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.username)