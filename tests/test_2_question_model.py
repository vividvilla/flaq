import unittest
from sqlalchemy.exc import InvalidRequestError

from flaq.models.user import User, Role
from flaq.models.question import Question, Tag

class QuestionTagTest(unittest.TestCase):

    def setUp(self):
        """Initalize with dummy details"""

        self.username = 'testuser'
        self.email = 'testuser@gmail.com'
        self.password = 'testpassword'
        self.real_name = 'testusername'
        self.bio = 'userbio'
        self.website = 'test.com'

        #CREATE default user role
        Role('user').create()

        #Insert all other optional parameters and check the value
        self.user = User(self.username)
        self.user.password = self.password
        self.user.email = self.email
        self.user.real_name = self.real_name
        self.user.bio = self.bio
        self.user.website = self.website
        self.user.create()

    def tearDown(self):
        User(self.username).delete()
        Role('user').delete()

    def test_tags(self):
        self.assertTrue(Tag('tag1').create())

        self.assertTrue(Tag.get('tag1').title == 'tag1')
        self.assertFalse(Tag.get('tag3'))

        self.assertTrue(Tag.get_objects(['tag1']) == [Tag.get('tag1')])
        self.assertTrue(
            Tag.get_objects(['tag1', 'tag2']) == [Tag.get('tag1'), Tag.get('tag2')])

        self.assertTrue(Tag('tag1').delete())
        self.assertTrue(Tag('tag2').delete())

        with self.assertRaises(ValueError):
            Tag('tag5').delete()

    def test_create_question(self):
        try:
            self.test_tags()
        except Exception as e:
            self.fail("{} failed ({}: {})".format(step, type(e), e))

        qid = Question(
                title = 'title',
                body = 'body',
                user = self.user,
                tags = ['tag1', 'tag2']).create().id

        self.assertTrue(Question().delete(qid))

    def test_get_question(self):
        return True

    def test_edit_question(self):
        return True

    def test_modify_question_tags(self):
        return True

    def delete_question(self):
        return True

if __name__ == '__main__':
    unittest.main()