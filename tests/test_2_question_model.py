import unittest
from sqlalchemy.orm.exc import NoResultFound

from flaq.models.user import User, Role
from flaq.models.question import Question, Tag
from flaq.utils import slugify

class QuestionTagTest(unittest.TestCase):

    def setUp(self):
        """Initalize with dummy details"""

        self.username = 'testuser'
        self.email = 'testuser@gmail.com'
        self.password = 'testpassword'
        self.real_name = 'testusername'
        self.bio = 'userbio'
        self.website = 'test.com'

        self.other_username = 'other_testuser'
        self.other_email = 'other_testuser@gmail.com'
        self.other_password = 'other_testpassword'

        #CREATE default user role
        Role('user').add()

        #Insert all other optional parameters and check the value
        self.user = User(self.username)
        self.user.password = self.password
        self.user.email = self.email
        self.user.real_name = self.real_name
        self.user.bio = self.bio
        self.user.website = self.website
        self.user.add()

        self.other_user = User(self.other_username)
        self.other_user.password = self.other_password
        self.other_user.email = self.other_email
        self.other_user.add()


    def tearDown(self):
        User(self.username).delete()
        User(self.other_username).delete()
        Role('user').delete()

    def test_tags(self):
        self.assertTrue(Tag('tag1').add())

        self.assertTrue(Tag.get('tag1').title == 'tag1')
        self.assertIsNone(Tag.get('tag3'))

        self.assertListEqual(Tag.get_objects(['tag1']), [Tag.get('tag1')])
        self.assertListEqual(
            Tag.get_objects(['tag1', 'tag2']), [Tag.get('tag1'), Tag.get('tag2')])

        self.assertTrue(Tag('tag1').delete())
        self.assertTrue(Tag('tag2').delete())

        with self.assertRaises(ValueError):
            Tag('tag5').delete()

    def test_create_question(self):

        try:
            self.test_tags()
        except Exception as e:
            self.fail("{} failed ({}: {})".format(step, type(e), e))

        #Create questions
        qid = Question(
                title = 'title',
                body = 'body',
                user = self.user,
                tags = ['tag1', 'tag2']).add().id

        #Get question
        self.assertTrue(Question.get(qid))
        self.assertTrue(Question.get(qid).title == 'title')
        self.assertTrue(Question.get(qid).body == 'body')
        self.assertIs(Question.get(qid).user, self.user)
        self.assertListEqual(
            Question.get(qid).tags, [Tag.get('tag1'), Tag.get('tag2')])

        with self.assertRaises(NoResultFound):
            Question.get(100).title

        #Adding tags to question
        self.assertListEqual(
            Question.get(qid).add_tags(qid, ['tag3']).tags,
                    [Tag.get('tag1'), Tag.get('tag2'), Tag.get('tag3')])

        #Deleting tags from question
        self.assertListEqual(
            Question.get(qid).remove_tags(qid, ['tag3']).tags,
                    [Tag.get('tag1'), Tag.get('tag2')])

        self.assertListEqual(
            Question.get(qid).remove_tags(qid, ['tag1', 'tag2']).tags, [])

        #Edit question
        self.assertTrue(
            Question().edit(qid, title = 'new title').title == 'new title')

        self.assertTrue(
            Question().edit(qid, title = 'new title').slug == slugify('new title'))

        self.assertTrue(
            Question().edit(qid, body = 'new body').body == 'new body')

        self.assertTrue(
            Question().edit(qid, slug = 'new body').slug == slugify('new body'))

        self.assertIsNone(Question().edit(qid))

        #Change User
        self.assertIs(
            Question().change_user(qid, self.other_user).user, self.other_user)

        #Delete question
        self.assertTrue(Question().delete(qid))

        #Delete above created tags
        Tag('tag1').delete()
        Tag('tag2').delete()
        Tag('tag3').delete()

if __name__ == '__main__':
    unittest.main()