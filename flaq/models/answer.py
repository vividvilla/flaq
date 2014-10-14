import datetime
import warnings
from sqlalchemy.orm.exc import NoResultFound

from flaq import db
from flaq import utils

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text, nullable = False)
    answer_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)

    def __init__(self, **details):
        self.body = details.get('body')
        self.user = details.get('user')
        self.question = details.get('question')

    def add(self):
        self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get(cls, answer_id):
        answer = cls.query.filter_by(id = answer_id).one()
        return answer

    def delete(self, answer_id):
        answer = self.get(answer_id)
        db.session.delete(answer)
        db.session.commit()
        return answer_id

    def edit(self, answer_id, **details):
        answer = self.get(answer_id)
        answer.body = details.get('body', answer.body)
        self.modified_date = datetime.datetime.now()
        db.session.commit()
        return answer

    def change_user(self, answer_id, user):
        answer = self.get(answer_id)
        answer.user = user
        self.modified_date = datetime.datetime.now()
        db.session.commit()
        return answer