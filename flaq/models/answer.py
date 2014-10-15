import datetime
import warnings
from sqlalchemy.orm.exc import NoResultFound

from flaq import db
from flaq import utils
from question import Question

answer_votes = db.Table('answer_votes',
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', foreign_keys = question_id, backref = 'answers')
    answered_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    answered = db.relationship('Question',
        foreign_keys = answered_id, backref = db.backref("answer", uselist=False))
    users_voted = db.relationship('User', secondary=answer_votes,
        backref=db.backref('upvoted_answers', lazy='dynamic'))

    def __init__(self, **details):
        self.body = details.get('body')
        self.user = details.get('user')
        self.question = details.get('question')
        self.answered = details.get('answered')

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