import datetime
import warnings
from sqlalchemy.orm.exc import NoResultFound

from flaq import db
from flaq import utils

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id'))
)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(240), unique = True, nullable = False)
    body = db.Column(db.Text, nullable = False)
    slug = db.Column(db.String(300), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('questions', lazy='dynamic'))
    created_date = db.Column(db.DateTime)
    modified_date = db.Column(db.DateTime)

    def __init__(self):
        pass

    def create(self, title, body, user, slug = None, tags = []):
        self.title = title
        self.body = body
        self.user = user
        self.tags = Tag.get_objects(tags)
        self.created_date = datetime.datetime.now()
        self.modified_date = datetime.datetime.now()
        self.slug = utils.slugify(slug) if slug else utils.slugify(title)
        db.session.add(self)
        db.session.commit()

        return self

    @classmethod
    def get(cls, qid):
        question = cls.query.filter_by(id = qid).one()
        return question

    def delete(self, qid):
        question = self.get(qid)
        db.session.delete(question)
        db.session.commit()
        return qid

    def edit(self, qid, title = None, body = None, slug = None):
        question = self.get(qid)

        if not title and not body and not slug:
            return None

        if title and not slug:
            slug = title

        question.title = title if title else question.title
        question.body = body if body else question.body
        question.slug = utils.slugify(slug) if slug else question.slug

        return self._modify_commit(question)

    def change_user(self, qid, user):
        question = self.get(qid)
        question.user = user
        return self._modify_commit(question)

    def add_tags(self, qid, tags = []):
        question = self.get(qid)
        uniquetags = set(question.tags + Tag.get_objects(tags))
        question.tags = list(uniquetags)
        return self._modify_commit(question)

    def remove_tags(self, qid, tags = []):
        question = self.get(qid)
        current_tags = question.tags
        tag_instances = Tag.get_objects(tags)

        for tag in tag_instances:
            try:
                current_tags.remove(tag)
            except ValueError as e:
                warnings.warn("The input tag - '{}' doesn't linked to " \
                    "question(id : {})".format(tag.title, qid))

        question.tags = current_tags
        return self._modify_commit(question)

    def _modify_commit(self, question):
        question.modified_date = datetime.datetime.now()
        db.session.commit()
        return question

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), unique = True)

    def __init__(self, title):
        self.title = title

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def get(cls, title):
        try:
            tag = cls.query.filter_by(title = title).one()
        except NoResultFound as e:
            return None
        return tag

    @classmethod
    def get_objects(cls, tag_titles):
        result_tags = []
        for title in tag_titles:
            tag = cls.get(title)
            if tag:
                result_tags.append(tag)
            else:
                result_tags.append(cls(title).create())

        return result_tags