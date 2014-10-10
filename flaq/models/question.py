from flaq import db
from tag import Tag, tags

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(240))
    body = db.Column(db.Text)
    slug = db.Column(db.String(300), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('questions', lazy='dynamic'))

    def __init__(self,  **details):
        pass

    def create(self, **details):
        pass

    def delete(self, qid):
        pass

    def edit(self, **details):
        pass

    def add_tags(self, tags = []):
        pass