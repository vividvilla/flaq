import datetime
import warnings
from sqlalchemy.orm.exc import NoResultFound

from flaq import db

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(240), unique = True)
    body = db.Column(db.Text)
    slug = db.Column(db.String(300), unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('questions', lazy='dynamic'))
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.Datetime)

    def __init__(self):
        pass

    def create(self, title, body, user, tags = []):
        self.title = title
        self.body = body
        self.user = user
        self.tags = Tag.get_tags(tags)
        self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()

        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def get(cls, qid):
        question = cls.query.filter(id = qid).one()
        return question

    def delete(self, qid):
        question = self.get(qid)
        db.session.delete(question)
        db.session.commit()

    def edit(self, qid, title = None, body = None):
        pass

    def change_user(self, qid, user):
        pass

    def add_tags(self, qid, tags = []):
        question = self.get(qid)
        uniquetags = set(question.tags + Tag.get_tags(tags))
        question.tags = uniquetags
        db.session.commit()

    def remove_tags(self, qid, tags = []):
        question = self.get(qid)
        current_tags = question.tags
        tag_instances = Tag.get_tags(tags)

        for tag in tag_instances:
            try:
                current_tags.remove(tag)
            except ValueError as e:
                warnings.warn("The input tag - '{}' doesn't linked to \
                    question({})".format(tag.title, qid))
        question.tags = current_tags

        db.session.commit()

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)

    def __init__(self, title):
        self.title = title

    @classmethod
    def get(cls, title):
        try:
            tag = cls.query.filter(title = title).one()
        except NoResultFound as e:
            return None
        return tag

    @classmethod
    def get_tags(cls, tag_titles):
        result_tags = []
        for title in tag_titles:
            tag_instance = cls(title)
            tag = tag_instance.get(title)
            if tag:
                result_tags.append(tag)
            else:
                result_tags.append(tag_instance)

        return result_tags