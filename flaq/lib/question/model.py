from flaq import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_ley = True)
    title = db.Column(db.String(240))
    body = db.Column(db.Text)
    slug = db.Column(db.String(300), unique = True)